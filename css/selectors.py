from dataclasses import dataclass, field
import re
from typing import Any, Optional
from history import HistoryManager
from enum import Enum
from html_parser import LINK_TAGS, Element, get_document

# https://www.w3.org/TR/selectors-4/


class PseudoClass(Enum):
    IS = "is"
    NOT = "not"
    HAS = "has"
    WHERE = "where"
    VISITED = "visited"
    HOVER = "hover"
    NTH_CHILD = "nth-child"
    NTH_LAST_CHILD = "nth-last-child"
    # etc...
    # ACTIVE = "active"
    # LANG = "lang"


class AttributeMatch(Enum):
    HAS_ATTR = ""
    EXACT_MATCH = "="
    CONTAINS_WORD = "~="
    CONTAINS_STRING = "*="
    DASH_END = "|="
    PREFIX_MATCH = "^="
    SUFFIX_MATCH = "$="


class Combinator(Enum):
    NONE = ""
    DESCENDANT = " "
    CHILD = ">"
    NEXT_SIBLING = "+"
    SUBSEQUENT_SIBLING = "~"
    COLUMN = "||"


class SimpleSelector:
    pass

# sum a given list of specificity tuples
def add_specs(specs):
    a = b = c = 0
    for sa, sb, sc in specs:
        a += sa
        b += sb
        c += sc
    return (a, b, c)


@dataclass
class Selector:
    """(num_ids, num_classes, num_tags) - for priority calculation"""

    specificity: tuple[int, int, int] = field(init=False)
    invalid: bool = field(default=False, init=False)


@dataclass
class UniversalSelector(Selector, SimpleSelector):
    namespace: Optional[str] = None

    def __post_init__(self):
        self.specificity = (0, 0, 0)

    def __str__(self):
        return "*"


@dataclass
class TypeSelector(Selector, SimpleSelector):
    tag: str
    namespace: Optional[str] = None

    def __post_init__(self):
        self.specificity = (0, 0, 1)

    def __str__(self):
        return self.tag


@dataclass
class AttributeSelector(Selector, SimpleSelector):
    att: str
    oper: AttributeMatch
    val: Optional[str] = None
    modifier: Optional[str] = None
    namespace: Optional[str] = None

    def __post_init__(self):
        self.specificity = (0, 1, 0)

    def __str__(self):
        oper = f" {self.oper.value} " if self.oper != AttributeMatch.HAS_ATTR else ""
        modifier = f" {self.modifier}" if self.modifier else ""
        val = self.val if self.val else ""
        return f"[{self.att}{oper}{val}{modifier}]"


@dataclass
class IDSelector(Selector, SimpleSelector):
    ID: str

    def __post_init__(self):
        self.specificity = (1, 0, 0)

    def __str__(self):
        return f"#{self.ID}"


@dataclass
class ClassSelector(Selector, SimpleSelector):
    class_: str

    def __post_init__(self):
        self.specificity = (0, 1, 0)

    def __str__(self):
        return f".{self.class_}"


@dataclass
class PseudoClassSelector(Selector, SimpleSelector):
    name: str
    args: Optional[Any]  # only if function type
    type: PseudoClass | None = field(init=False)

    # https://www.w3.org/TR/selectors-4/#specificity-rules
    def __post_init__(self):
        self.type = PseudoClass._value2member_map_.get(self.name)
        specificity = (0, 1, 0)
        match self.type:
            case PseudoClass.IS, PseudoClass.NOT, PseudoClass.HAS:
                if self.args:
                    specificity = max(s.specificity for s in self.args)
            case PseudoClass.WHERE:
                specificity = (0, 0, 0)
            case PseudoClass.NTH_CHILD, PseudoClass.NTH_LAST_CHILD:
                if self.args:
                    specificity = list(max(s.specificity for s in self.args))
                    specificity[1] += 1
                    specificity = tuple(specificity)
        self.specificity = specificity

    def __str__(self):
        args_str = f"({", ".join(str(s) for s in self.args)})" if self.args else ""
        return f":{self.type}{args_str}"


@dataclass
class PseudoElement:
    name: str
    args: Optional[Any]  # only if function type
    pseudo_classes: list[PseudoClassSelector]

    def pseudo_classes_specificity(self):
        return add_specs(s.specificity for s in self.pseudo_classes)


@dataclass
class CompoundSelector(Selector):  # Similar to SelectorSequence in the book
    # first selector in sequence must be of type TypeSelector or UniversalSelector
    selectors: list[SimpleSelector]
    pseudo_element_chain: list[PseudoElement]

    # combinator is placed here instead of ComplexSelector
    # has no impact on a lone CompoundSelector, only when within ComplexSelector
    # applies left side of our compound selector, so for example
    # ComplexSelector = OtherCompoundSelector [combinator ThisCompoundSelector]
    combinator: Combinator = Combinator.NONE

    def __post_init__(self):
        selectors_specificity = add_specs(s.specificity for s in self.selectors)
        pseudo_specificity = add_specs(
            s.pseudo_classes_specificity() for s in self.pseudo_element_chain
        )
        self.specificity = add_specs([selectors_specificity, pseudo_specificity])

    def __str__(self):
        return "".join(str(selector) for selector in self.selectors)


@dataclass
class ComplexSelector(Selector):
    compound_selectors: list[CompoundSelector]

    def __post_init__(self):
        self.specificity = tuple(
            sum(values)
            for values in zip(*(s.specificity for s in self.compound_selectors))
        )

    def __str__(self):
        return "".join(
            str(s) + (f" {s.combinator} " if s.combinator else "")
            for s in self.compound_selectors
        )


class SelectorMatcher:
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager

    def matches(self, selector: Selector, node: Element) -> bool:
        if not isinstance(node, Element):
            return False
        match selector:
            case UniversalSelector():
                return True
            case TypeSelector(tag=tag):
                return node.tag == tag
            case AttributeSelector():
                return self._matches_attribute(selector, Element)
            case IDSelector(ID=ID):
                return ID == node.attributes.get("id")
            case ClassSelector(classes=classes):
                return all(c in node.classes for c in classes)
            case PseudoClassSelector():
                return self._matches_pseudoclass(selector, Element)
            case CompoundSelector(selectors=selectors):
                return all(self.matches(s, node) for s in selectors)
            case ComplexSelector():
                return self._matches_complex(selector, node)
            case _:
                pass

    def _matches_attribute(self, selector: AttributeSelector, node: Element):
        att, val = selector.att, selector.val
        match selector.oper:
            case AttributeMatch.HAS_ATTR:
                return att in node.attributes
            case AttributeMatch.EXACT_MATCH:
                return val and val == node.attributes.get(att)
            case AttributeMatch.CONTAINS_WORD:
                node_att = node.attributes.get(att)
                return val and any(v in node_att for v in val.split(" "))
            case AttributeMatch.CONTAINS_STRING:
                return val and val in node.attributes.get(att)
            case AttributeMatch.DASH_END:
                return val and re.match(rf"^{val}.*-$", node.attributes.get(att))
            case AttributeMatch.PREFIX_MATCH:
                return val and node.attributes.get(att).startswith(val)
            case AttributeMatch.SUFFIX_MATCH:
                return val and node.attributes.get(att).endswith(val)
            case _:
                raise f"{selector.oper} not a valid attribute match operation for {str(selector)}!"

    def _matches_pseudoclass(self, selector: PseudoClassSelector, node: Element):
        match selector.type:
            case PseudoClass.IS, PseudoClass.WHERE:
                return selector.args != [] and any(
                    s.matches(node) for s in selector.args
                )
            case PseudoClass.NOT:
                return selector.args != [] and not any(
                    s.matches(node) for s in selector.args
                )
            case PseudoClass.HAS:
                return self._matches_has(selector, node)
            case PseudoClass.VISITED:
                if node.tag in LINK_TAGS and "href" in node.attributes:
                    document = get_document(node)
                    resolved_url = document.url.resolve(node.attribute["href"])
                    return self.history_manager.has_url(resolved_url)
            case _:
                raise f"{selector.type} not a valid selector type for {str(selector)}!"

    def _matches_complex(self, selector: ComplexSelector, node: Element):

        def recurse(elem: Element, idx: int) -> bool:
            # match right to left
            # example: div ~ article p

            # <div></div>
            # <br>
            # <article>
            #     <div>
            #         <p> I'm matched </p>
            #     </div>
            # </article>

            # match p:          recurse(2, p):                      oper = None, p matched, continue
            # match article:    recurse(1, elem):                   oper =  , article matched at elem.parent.parent, continue
            # match div:        recurse(0, elem.parent.parent):     oper = ~, div matched at elem.parent.children[:cur_idx], continue
            # match -1: return True
            if idx < 0:
                return True

            s = selector.compound_selectors[idx]

            match s.combinator:
                case Combinator.NONE:
                    if not self.matches(s, elem):
                        return False
                    return recurse(elem, idx - 1)

                case Combinator.DESCENDANT:
                    cur = elem.parent
                    while cur:
                        if self.matches(cur, elem):
                            return recurse(idx - 1, cur)
                        s = s.parent
                    return False

                case Combinator.CHILD:
                    if not self.matches(s, elem.parent):
                        return False
                    return recurse(idx - 1, s.parent)

                case Combinator.NEXT_SIBLING:
                    siblings = elem.parent.children
                    sibling_elem_idx = siblings.index(elem)
                    if sibling_elem_idx == -1:
                        return False
                    if not any(
                        self.matches(s, sibling)
                        for sibling in siblings[:sibling_elem_idx]
                    ):
                        return False
                    return recurse(idx - 1, s)

                case Combinator.SUBSEQUENT_SIBLING:
                    siblings = elem.parent.children
                    sibling_elem_idx = siblings.index(elem)
                    if sibling_elem_idx <= 0:
                        return False
                    if not self.matches(s, siblings[sibling_elem_idx - 1]):
                        return False
                    return recurse(idx - 1, cur)

        return recurse(node, len(selector.compound_selectors) - 1)

    # =========== Specific Pseudo Class Selector Matching =========== #

    def _matches_has(self, selector: PseudoClass, node: Element):
        # a proper implementation would walk right to left and call a restyle on matched parents
        # but I'll skip this optimization for small static sites
        for child in node.children:
            for s in selector.args:
                if self.matches(s, child):
                    return True
            if self._matches_has(selector, child):
                return True


def rightmost_selector(selector: Selector) -> Selector:
    if not isinstance(selector, (CompoundSelector, ComplexSelector)):
        return selector

    elif isinstance(selector, CompoundSelector):
        for i in range(len(selector.selectors)-1, -1, -1):
            # only HAS and EXACT MATCH attribute selectors should be indexed for performance reasons
            if isinstance(selector.selectors[i], AttributeSelector):
                if selector.selectors[i].oper == AttributeMatch.HAS_ATTR or selector.selectors[-1].oper == AttributeMatch.EXACT_MATCH:
                    return selector.selectors[i]
            return selector.selectors[i]

    return rightmost_selector(selector.compound_selectors[-1])


            
            

            


    
