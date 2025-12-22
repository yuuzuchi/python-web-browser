from css.property import property_is_inherited
from css.style_values.keyword import KeywordValue
from history import HistoryManager
from css.selector_matcher import SelectorMatcher
from css.selector_index import SelectorIndex
from css.stylesheet import CSSStylesheet
from css.style_rule import StyleRule
from css.parser import CSSSyntaxParser
from dom import Document, Node, Element, Text
from css.enums import Keyword, Origin, Property
from css.parse_context import ParseContext
from css.initial_value_cache import property_initial_value
from log import log, set_debug

"""
This class is responsible for cascading and inheritance, and calculating the `Actual Values` for each DOM node. 
https://drafts.csswg.org/css-cascade-5/#filtering

TODO:
    preprocessing:
    1. get each rule to hold its origin source, as well as source index
        - source index should be a global counter variable, maybe store on the document? 
        - or inject a ParseContext object that holds the counter
    2. combine all rules into a giant list[StyleRule]
    3. build index

    value processing:
    1. Filtering(list[StyleRule]) -> list[Declaration]
        - gather all applicable rules (from index)
        - call matcher on each node (using build_index) and places a list of candidate declarations on every node

    2. cascade 
        - iterate through rules (in cascade order), and each declaration within, building a map of winning properties
"""


class StyleComputer:
    def __init__(
        self,
        DOM: Document,
        stylesheets: list[CSSStylesheet],
        history_manager: HistoryManager,
    ):
        self.selector_index = SelectorIndex()
        self.selector_matcher = SelectorMatcher(history_manager)
        self.stylesheets = stylesheets
        self.DOM = DOM

    def style_tree(self) -> None:
        # build our index
        for stylesheet in self.stylesheets:
            self.selector_index.build_index_for_rules(stylesheet.rules)

        # filter, match, cascade
        self.match_and_cascade(self.DOM.document_element)

        # defaulting
        self.compute_defaults(self.DOM.document_element)

        self.print_tree()

    def match_and_cascade(self, node: Element) -> None:
        """For each element in the DOM, produce a list of candidate rules through selector matching.
        Then, iterate through rules (in cascade order), applying properties to each node with tiebreakers.
        """
        # gather candidate rules
        candidate_rules: list[StyleRule] = []
        for rule in self.selector_index.get_rules_for_node(node):
            for selector in rule.selector_list:
                if self.selector_matcher.matches(selector, node):
                    candidate_rules.append(rule)

        # parse and add any inline style attributes
        if style := node.attributes.get("style"):
            stylesheet = CSSSyntaxParser().parse_css_style_attribute(
                style, parse_context=ParseContext(Origin.AUTHOR_ORIGIN)
            )
            candidate_rules.extend(stylesheet.rules)
            del node.attributes["style"]

        # apply each rule's declarations
        # we do this in two passes, as important declarations have different origin priorities.
        # first pass: do only NON !important declarations with the rule's origin priority set to unimportant
        # second pass: do only !important declarations with the rule's origin priority set to important

        # first pass:
        # sort rules by cascade order (origin, specificity, then source order) in ascending order
        candidate_rules.sort(key=lambda m: m.get_sort_key(important=False))
        for rule in candidate_rules:
            for decl in rule.declarations:
                if decl.important:
                    continue
                node.style[decl.prop] = decl.val

        # second pass:
        candidate_rules.sort(key=lambda m: m.get_sort_key(important=True))
        for rule in candidate_rules:
            for decl in rule.declarations:
                if not decl.important:
                    continue
                node.style[decl.prop] = decl.val

        # recursively style children
        for child in node.children:
            if isinstance(child, Element):
                self.match_and_cascade(child)

    def compute_defaults(self, node: Node) -> None:
        """Compute inherited and initial properties"""
        # TODO: provide lazy compute method
        for prop in Property:
            if val := node.style.get(prop):
                if isinstance(val, KeywordValue) and val.is_css_wide:
                    # https://drafts.csswg.org/css-cascade-5/#defaulting-keywords
                    if val.keyword == Keyword.INHERIT:
                        self.inherit_property(node, prop)
                    elif val.keyword == Keyword.INITIAL:
                        self.initial_property(node, prop)
                    elif val.keyword == Keyword.UNSET:
                        if property_is_inherited(prop):
                            self.inherit_property(node, prop)
                        else:
                            self.initial_property(node, prop)
                    elif val.keyword == Keyword.REVERT:
                        pass
                    elif val.keyword == Keyword.REVERT_LAYER:
                        pass
                        # TODO: need to store origin of each property

            elif property_is_inherited(prop):
                self.inherit_property(node, prop)

        for child in node.children:
            self.compute_defaults(child)

    def inherit_property(self, node: Node, prop: Property) -> None:
        if node.parent and (val := node.parent.style.get(prop)):
            node.style[prop] = val
        # elif not node.parent:
        #     self.initial_property(node, prop)

    # TODO: finish property/value parser so this doesn't immediately crash everything
    def initial_property(self, node: Node, prop: Property) -> None:
        if init := property_initial_value(prop):
            node.style[prop] = init

    def print_tree(self) -> None:
        def recurse(node: Node):
            if isinstance(node, Element):
                log(f"{node.tag}:")
            elif isinstance(node, Text):
                log(f"'{node.text}':")

            for key, val in node.style.items():
                log(f"    {key.value} = {val};")

            for child in node.children:
                recurse(child)

        recurse(self.DOM.document_element)


if __name__ == "__main__":
    set_debug()
    from html_parser import HTMLParser
    from css.parser import CSSSyntaxParser
    from css.enums import Origin
    from css.parse_context import ParseContext
    from url import URL

    html = """
    <html>
        <body>
            <h1>Title</h1>
            <div class="test">
                <p id="p">Hello World</p>
                <a href="https://example.com">Link</a>
            </div>
            <ul>
                <li><i>Item 1</i></li>
                <li><b>It<i>em</b> 2</i></li>
            </ul>
            <pre> hello </pre>
        </body>
    </html>
    """
    with open("css/browser.css", "r") as f:
        browser_css = f.read()

    user_css = """
    body h1 {
        color: red !important;
    }

    div.test{
        color: orange !important;
    }

    #p {
        color: purple !important;
    }
    """

    url = URL("file:///test.html")
    doc = HTMLParser(html, url).parse()

    parser = CSSSyntaxParser()
    stylesheet = parser.parse_css_stylesheet(
        browser_css, ParseContext(origin=Origin.USER_AGENT)
    )

    stylesheet2 = parser.parse_css_stylesheet(
        user_css, ParseContext(origin=Origin.AUTHOR_ORIGIN)
    )

    # expected output:
    # if neither important, user_css wins (pre)
    # if both important, browser_css wins (normal)
    # if one important, the important one wins

    history = HistoryManager()
    computer = StyleComputer(doc, [stylesheet, stylesheet2], history)
    computer.style_tree()
