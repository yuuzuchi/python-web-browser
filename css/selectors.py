from dataclasses import dataclass, field
import re
from typing import Any, Optional, cast
from enum import Enum


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


class SimpleSelector(Selector):
    pass


@dataclass
class UniversalSelector(SimpleSelector):
    namespace: Optional[str] = None

    def __post_init__(self):
        self.specificity = (0, 0, 0)

    def __str__(self):
        return "*"


@dataclass
class TypeSelector(SimpleSelector):
    # tag is case insensitive, parser will .casefold() it during creation
    tag: str
    namespace: Optional[str] = None

    def __post_init__(self):
        self.specificity = (0, 0, 1)

    def __str__(self):
        return self.tag


@dataclass
class AttributeSelector(SimpleSelector):
    # att is case insensitive, parser will .casefold() it during creation
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
class IDSelector(SimpleSelector):
    ID: str

    def __post_init__(self):
        self.specificity = (1, 0, 0)

    def __str__(self):
        return f"#{self.ID}"


@dataclass
class ClassSelector(SimpleSelector):
    class_: str

    def __post_init__(self):
        self.specificity = (0, 1, 0)

    def __str__(self):
        return f".{self.class_}"


@dataclass
class PseudoClassSelector(SimpleSelector):
    name: str
    args: Optional[Any]  # only if function type
    type: PseudoClass | None = field(init=False)

    # https://www.w3.org/TR/selectors-4/#specificity-rules
    def __post_init__(self):
        self.type = cast(
            PseudoClass | None, PseudoClass._value2member_map_.get(self.name)
        )
        specificity = (0, 1, 0)
        match self.type:
            case PseudoClass.IS | PseudoClass.NOT | PseudoClass.HAS:
                if self.args:
                    specificity = max(s.specificity for s in self.args)
            case PseudoClass.WHERE:
                specificity = (0, 0, 0)
            case PseudoClass.NTH_CHILD | PseudoClass.NTH_LAST_CHILD:
                if self.args:
                    specificity = list(max(s.specificity for s in self.args))
                    specificity[1] += 1
                    specificity = tuple(specificity)
        self.specificity = specificity

    def __str__(self):
        args_str = f"({", ".join(map(str, self.args))})" if self.args else ""
        name = self.type.value if self.type else self.name
        return f":{name}{args_str}"


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
        res = "".join(str(selector) for selector in self.selectors)
        for pe in self.pseudo_element_chain:
            res += f"::{pe.name}"
            if pe.pseudo_classes:
                res += "".join(str(pc) for pc in pe.pseudo_classes)
        return res


@dataclass
class ComplexSelector(Selector):
    compound_selectors: list[CompoundSelector]

    def __post_init__(self):
        self.specificity = add_specs(s.specificity for s in self.compound_selectors)

    def __str__(self):
        res = ""
        for i, s in enumerate(self.compound_selectors):
            res += str(s)
            if i < len(self.compound_selectors) - 1:
                comb = self.compound_selectors[i + 1].combinator
                if comb == Combinator.DESCENDANT:
                    res += " "
                elif comb != Combinator.NONE:
                    res += f" {comb.value} "
        return res


def rightmost_selector(selector: Selector) -> Selector:
    if not isinstance(selector, (CompoundSelector, ComplexSelector)):
        return selector

    elif isinstance(selector, CompoundSelector):
        for i in range(len(selector.selectors) - 1, -1, -1):
            # only HAS and EXACT MATCH attribute selectors should be indexed for performance reasons
            sel = selector.selectors[i]
            if isinstance(sel, AttributeSelector):
                if (
                    sel.oper == AttributeMatch.HAS_ATTR
                    or sel.oper == AttributeMatch.EXACT_MATCH
                ):
                    return selector.selectors[i]
            return selector.selectors[i]

    assert isinstance(selector, ComplexSelector)
    return rightmost_selector(selector.compound_selectors[-1])
