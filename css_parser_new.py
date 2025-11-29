from history import HistoryManager
from html_parser import Element, Text
from dataclasses import dataclass, field

from lexer import Lexer, Token

DEBUG = False

INHERITED_PROPERTIES = {
    "font-size": "16px",
    "font-style": "normal",
    "font-weight": "normal",
    "font-family": "Segoe UI",
    "color": "black",
    "white-space": "normal",
}

INITIAL_PROPRETIES = {
    # Positioning & Layout
    "display": "inline",
    "position": "static",
    "z-index": "auto",
    "top": "auto",
    "right": "auto",
    "bottom": "auto",
    "left": "auto",
    "float": "none",
    "clear": "none",
    # Box Model
    "box-sizing": "content-box",
    "margin-top": "0",
    "margin-right": "0",
    "margin-bottom": "0",
    "margin-left": "0",
    "padding-top": "0",
    "padding-right": "0",
    "padding-bottom": "0",
    "padding-left": "0",
    "border-width": "medium",
    "border-style": "none",
    "border-color": "currentcolor",
    "border-radius": "0",
    # Background
    "background-color": "transparent",
    "background-image": "none",
    "background-repeat": "repeat",
    "background-position-x": "0%",
    "background-position-y": "0%",
    "background-size": "auto",
    "background-attachment": "scroll",
    "background-clip": "border-box",
    "background-origin": "padding-box",
    # Sizing
    "width": "auto",
    "min-width": "0",
    "max-width": "none",
    "height": "auto",
    "min-height": "0",
    "max-height": "none",
    # Typography
    "font-style": "normal",
    "font-variant": "normal",
    "font-weight": "normal",
    "font-stretch": "normal",
    "font-size": "medium",
    "font-family": "initial",  # no universal fixed value — depends on UA
    "line-height": "normal",
    "text-align": "start",  # CSS3; CSS2 had 'left' for LTR
    "text-decoration-line": "none",
    "text-transform": "none",
    "letter-spacing": "normal",
    "word-spacing": "normal",
    "white-space": "normal",
    "vertical-align": "baseline",
    "text-indent": "0",
    "direction": "ltr",
    # Color & Visibility
    "color": "initial",  # UA dependent, often black
    "opacity": "1",
    "visibility": "visible",
    # List Style
    "list-style-type": "disc",
    "list-style-image": "none",
    "list-style-position": "outside",
    # Tables
    "border-collapse": "separate",
    "border-spacing": "0",
    "caption-side": "top",
    "table-layout": "auto",
    # Overflow
    "overflow-x": "visible",
    "overflow-y": "visible",
    # Flexbox
    "flex-direction": "row",
    "flex-wrap": "nowrap",
    "flex-grow": "0",
    "flex-shrink": "1",
    "flex-basis": "auto",
    "align-items": "stretch",
    "justify-content": "flex-start",
    "align-content": "stretch",
    # Grid
    "grid-template-columns": "none",
    "grid-template-rows": "none",
    "grid-auto-flow": "row",
    "grid-auto-columns": "auto",
    "grid-auto-rows": "auto",
    # Transitions & Animation
    "transition-property": "all",
    "transition-duration": "0s",
    "transition-timing-function": "ease",
    "transition-delay": "0s",
    "animation-name": "none",
    "animation-duration": "0s",
    "animation-timing-function": "ease",
    "animation-iteration-count": "1",
    "animation-direction": "normal",
    "animation-fill-mode": "none",
    "animation-play-state": "running",
    # Transforms
    "transform": "none",
    "transform-origin": "50% 50% 0",
}

# font shorthand keywords
STYLE = {"italic", "oblique"}
VARIANT = {"small-caps"}
WEIGHT = {"bold", "bolder", "lighter"}
STRETCH = {
    "condensed",
    "expanded",
    "semi-condensed",
    "extra-condensed",
    "extra-expanded",
    "ultra-condensed",
    "ultra-expanded",
}
SIZE = {"px", "pt", "em", "rem", "%", "vh", "vw"}

@dataclass
class Declaration:
    prop: str
    val: str
    important: bool
    origin_priority: int
    rule_order: int
    sort_key: tuple | None = field(default=None, init=False)

    def with_specificity(self, specificity):
        decl = Declaration(
            self.prop, self.val, self.important, self.origin_priority, self.rule_order
        )
        decl.sort_key = (
            self.important,
            self.origin_priority,
            specificity,
            self.rule_order,
        )
        return decl

    def set_specificity(self, specificity):
        self.specificity = specificity
        self.sort_key = (
            self.important,
            self.origin_priority,
            specificity,
            self.rule_order,
        )

    def __str__(self):
        return f"{self.prop}: {self.val}{" !important" if self.important else ""};"


@dataclass
class Rule:
    selector: Selector
    declarations: list[Declaration]

    def __str__(self):
        return f"{str(self.selector)}\n{"\n".join("  " + str(decl) for decl in self.declarations)}"


class CSSParser:

    def __init__(self, s: str, history_manager: HistoryManager, tok_iter=None):
        """If tok_iter is specified, parser will ignore s and use the token list instead"""
        if not tok_iter and s:
            tok_iter = Lexer(s, history_manager).parse()
        self.tok_iter = tok_iter
        self.cur, self.next = next(self.tok_iter), next(self.tok_iter)

    def consume(self) -> Token:
        # load next token, return current
        res = self.cur
        self.cur = self.next
        self.next = next(self.tok_iter)
        return res

    def parse(
        self, origin_priority, s=None
    ) -> list[Rule]:  # if passed s argument, reset s and i for new text
        if s:
            self.s = s
            self.i = 0

        rules = []
        self.whitespace()
        while self.i < len(self.s):
            try:
                selectors = self.selectors()
                self.literal("{")
                self.whitespace()
                body = self.body(origin_priority)
                self.literal("}")
                for selector in selectors:
                    body_copy = [
                        decl.with_specificity(selector.specificity) for decl in body
                    ]
                    rules.append(Rule(selector, body_copy))
                self.whitespace()
            except Exception as e:
                if DEBUG:
                    print("Parse,", e)
                why = self.consume_until(["}"])
                if why == "}":
                    self.literal("}")
                    self.whitespace()
                else:
                    break
        return rules

    def _font_shorthand(self, val):
        # default values
        pairs = {
            "font-style": "normal",
            "font-variant": "normal",
            "font-weight": "normal",
            "font-stretch": "normal",
            "line-height": "1.5",
        }
        # look for font-size (mandatory), ends with size unit
        size_idx = -1
        for i in range(len(val)):
            for unit in SIZE:
                if val[i].endswith(unit):
                    pairs["font-size"] = val[i]
                    size_idx = i
        # match style, variant, weight, stretch before size_idx
        for i in range(size_idx):
            if val[i] in STYLE:
                pairs["font-style"] = val[i]
            elif val[i] in VARIANT:
                pairs["font-variant"] = val[i]
            elif val[i] in WEIGHT:
                pairs["font-weight"] = val[i]
            elif val[i].isdigit():
                pairs["font-weight"] = int(val[i])
            elif val[i] in STRETCH:
                pairs["font-stretch"] = val[i]
        # line-height
        if size_idx < len(val) - 2:
            pairs["line-height"] = float(val[size_idx + 1][1:])
        pairs["font-family"] = val[-1]
        return pairs

    # To style the entire node tree, we need to do two passes
    # First pass to read all <style> tags and add them to our rules
    # Second to actually compute styles for each node
    # Time complexity:
    def style(self, node, rules):
        def parse_styletags(node):
            if isinstance(node, Text) and node.parent.tag == "style":
                styletag_rules = self.parse(origin_priority=2, s=node.text)
                rules.extend(styletag_rules)

            for child in node.children:
                parse_styletags(child)

        def _style(node):
            candidates = []
            # get sheet rules
            for rule in rules:
                selector, declarations = rule.selector, rule.declarations
                if not selector.matches(node):
                    continue
                candidates.extend(declarations)

            # get any style attribute rules
            if isinstance(node, Element) and "style" in node.attributes:
                declarations = CSSParser(
                    node.attributes["style"], self.history_manager
                ).body(3, specificity=(0, 0, 0))
                candidates.extend(declarations)

            # add styles to nodes
            final = {}
            for decl in candidates:
                prop = decl.prop
                if prop not in final or decl.sort_key > final[prop].sort_key:
                    final[prop] = decl

            # replace decl objects with their values
            node.style = {prop: decl.val for prop, decl in final.items()}

            # get inheritable properties from parents
            for prop, default in INHERITED_PROPERTIES.items():
                if prop in final:
                    continue
                elif node.parent:
                    node.style[prop] = node.parent.style[prop]
                else:
                    node.style[prop] = default

            _compute(node)

            for child in node.children:
                _style(child)

        parse_styletags(node)
        _style(node)


def _compute(node):
    # resolve 'inherit' and related keywords
    for prop, value in node.style.items():
        if value == "inherit":
            if prop in node.parent.style:
                node.style[prop] = node.parent.style[prop]
        elif value == "initial":
            if prop in INITIAL_PROPRETIES:
                node.style[prop] = INITIAL_PROPRETIES[prop]
        elif value == "unset":
            if prop in INHERITED_PROPERTIES and prop in node.parent.style:
                node.style[prop] = node.parent.style[prop]
            elif prop in INITIAL_PROPRETIES:
                node.style[prop] = INITIAL_PROPRETIES[prop]

    # compute font shorthand (font-size and font-family are required
    # font: [font-style] [font-variant] [font-weight] [font-stretch] font-size [/ line-height] font-family
    if "font" in node.style:
        pass

    # compute percentages to px values (to prevent inherited fonts from scaling off of parents again)
    if node.style["font-size"].endswith("%"):
        if node.parent:
            parent_font_size = node.parent.style["font-size"]
        else:
            parent_font_size = INHERITED_PROPERTIES["font-size"]
        node_pct = float(node.style["font-size"][:-1]) / 100
        parent_px = float(parent_font_size[:-2])
        node.style["font-size"] = str(node_pct * parent_px) + "px"


def print_sheet(s):
    parser = CSSParser(s)
    res = parser.parse(1)
    for rule in res:
        print(str(rule))
        print()


def print_rules(rules):
    for rule in rules:
        print(str(rule))
        print()


if __name__ == "__main__":
    DEBUG = True
    import sys

    f = "./browser.css"
    if len(sys.argv) > 1:
        f = sys.argv[1]

    with open(f, "r") as file:
        print_sheet(file.read())
