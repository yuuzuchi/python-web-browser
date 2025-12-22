import re
from dom import Node, Element
from history import HistoryManager
from log import err
from css.selectors import (
    Selector,
    UniversalSelector,
    TypeSelector,
    IDSelector,
    ClassSelector,
    AttributeSelector,
    PseudoClassSelector,
    CompoundSelector,
    ComplexSelector,
    AttributeMatch,
    PseudoClass,
    Combinator,
)
from html_parser import LINK_TAGS, Element, get_document


class SelectorMatcher:
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager

    def matches(self, selector: Selector, node: Node) -> bool:
        if not isinstance(node, Element):
            return False
        match selector:
            case UniversalSelector():
                return True
            case TypeSelector(tag=tag):
                return node.tag == tag
            case AttributeSelector():
                return self._matches_attribute(selector, node)
            case IDSelector(ID=ID):
                return ID == node.attributes.get("id")
            case ClassSelector(class_=class_):
                return class_ in node.classes
            case PseudoClassSelector():
                return self._matches_pseudoclass(selector, node)
            case CompoundSelector(selectors=selectors):
                return all(self.matches(s, node) for s in selectors)
            case ComplexSelector():
                return self._matches_complex(selector, node)
            case _:
                return False

    def _matches_attribute(self, selector: AttributeSelector, node: Element) -> bool:
        att, val = selector.att, selector.val
        match selector.oper:
            case AttributeMatch.HAS_ATTR:
                return att in node.attributes
            case AttributeMatch.EXACT_MATCH:
                return bool(val and val == node.attributes.get(att))
            case AttributeMatch.CONTAINS_WORD:
                node_att = node.attributes.get(att, "")
                return bool(val and any(v in node_att for v in val.split(" ")))
            case AttributeMatch.CONTAINS_STRING:
                return bool(val and val in node.attributes.get(att, ""))
            case AttributeMatch.DASH_END:
                return bool(
                    val and re.match(rf"^{val}.*-$", node.attributes.get(att, ""))
                )
            case AttributeMatch.PREFIX_MATCH:
                return bool(val and node.attributes.get(att, "").startswith(val))
            case AttributeMatch.SUFFIX_MATCH:
                return bool(val and node.attributes.get(att, "").endswith(val))
            case _:
                err(
                    f"{selector.oper} not a valid attribute match operation for {str(selector)}!"
                )
                return False

    def _matches_pseudoclass(
        self, selector: PseudoClassSelector, node: Element
    ) -> bool:
        match selector.type:
            case PseudoClass.IS | PseudoClass.WHERE:
                if not selector.args:
                    return False
                return selector.args != [] and any(
                    s.matches(node) for s in selector.args
                )
            case PseudoClass.NOT:
                if not selector.args:
                    return False
                return selector.args != [] and not any(
                    s.matches(node) for s in selector.args
                )
            case PseudoClass.HAS:
                return self._matches_has(selector, node)
            case PseudoClass.VISITED:
                # return True
                if node.tag in LINK_TAGS and "href" in node.attributes:
                    document = get_document(node)
                    resolved_url = document.url.resolve(node.attributes["href"])
                    return self.history_manager.has_url(resolved_url)
            case _:
                err(f"{selector.type} not a valid selector type for {str(selector)}!")
                return False
        return False

    def _matches_complex(self, selector: ComplexSelector, node: Element) -> bool:
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
                        if self.matches(s, elem):
                            return recurse(cur, idx - 1)
                        cur = cur.parent
                    return False

                case Combinator.CHILD:
                    if not self.matches(s, elem.parent):
                        return False
                    return recurse(elem.parent, idx - 1)

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
                    return recurse(elem, idx - 1)

                case Combinator.SUBSEQUENT_SIBLING:
                    siblings = elem.parent.children
                    sibling_elem_idx = siblings.index(elem)
                    if sibling_elem_idx <= 0:
                        return False
                    if not self.matches(s, siblings[sibling_elem_idx - 1]):
                        return False
                    return recurse(elem, idx - 1)

                case _:
                    return False

        return recurse(node, len(selector.compound_selectors) - 1)

    # =========== Specific Pseudo Class Selector Matching =========== #

    def _matches_has(self, selector: PseudoClassSelector, node: Element) -> bool:
        # a proper implementation would walk right to left and call a restyle on matched parents
        # but I'll skip this optimization for small static sites
        for child in node.children:
            if not selector.args or not isinstance(child, Element):
                continue

            for s in selector.args:
                if self.matches(s, child):
                    return True
            if self._matches_has(selector, child):
                return True

        return False
