from collections import defaultdict
from css.style_rule import StyleRule
from css.selectors import (
    IDSelector,
    ClassSelector,
    TypeSelector,
    AttributeMatch,
    AttributeSelector,
    PseudoClassSelector,
    UniversalSelector,
    rightmost_selector,
)
from dom import Element


class SelectorIndex:
    def __init__(self):
        self.id_dict = defaultdict(list)
        self.class_dict = defaultdict(list)
        self.type_dict = defaultdict(list)
        self.attr_dict = defaultdict(list)
        self.attr_eq_dict = defaultdict(list)
        self.universal_list = list()

    def build_index_for_rules(self, rules: list[StyleRule]) -> None:
        """
        Given a list of style rules, create an index mapping rightmost selector -> rule

        For example, if given `rule1 = div#a {...}`, id_dict would look like `{"a": {rule1}}`
        """
        for rule in rules:
            for selector in rule.selector_list:
                rightmost = rightmost_selector(selector)
                match rightmost:
                    case IDSelector():
                        self.id_dict[rightmost.ID].append(rule)
                    case ClassSelector():
                        self.class_dict[rightmost.class_].append(rule)
                    case TypeSelector():
                        self.type_dict[rightmost.tag].append(rule)
                    case AttributeSelector():
                        if rightmost.oper == AttributeMatch.HAS_ATTR:
                            self.attr_dict[rightmost.att].append(rule)
                        elif rightmost.oper == AttributeMatch.EXACT_MATCH:
                            self.attr_eq_dict[(rightmost.att, rightmost.val)].append(
                                rule
                            )
                        else:
                            self.universal_list.append(rule)
                    case UniversalSelector() | PseudoClassSelector():
                        self.universal_list.append(rule)
                    case _:
                        raise AssertionError(f"unrecognized selector type {selector}")

    def get_rules_for_node(self, node: Element) -> list[StyleRule]:
        assert isinstance(node, Element)
        """
        Given a single node, return any possible rules that may match it.
        These rules do **NOT** necessarily target the node, but produces a filtered list of rules to run the selector matcher against.
        """
        out = set(self.universal_list)
        out.update(self.type_dict.get(node.tag, []))

        for att, val in node.attributes.items():
            if att == "id":
                out.update(self.id_dict.get(att, []))
            if val:
                out.update(self.attr_eq_dict.get((att, val), []))
            out.update(self.attr_dict.get(att, []))

        for class_ in node.classes:
            out.update(self.class_dict.get(class_, []))

        return list(out)
