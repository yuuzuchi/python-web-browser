from dom import Document, Node, Element, Text
from font_cache import get_font
from history import HistoryManager
from css.style_values.numeric import NumberValue
from css.style_values.string import StringValue
from css.style_values.custom_ident import CustomIdentValue
from css.style_values.list import ListStyleValue
from css.units import LengthUnit
from css.style_values.dimension import PercentageValue, Length, LengthValue
from css.enums import (
    FONT_SIZE_SCALING_TABLE,
    AbsoluteSize,
    RelativeSize,
    Keyword,
    Origin,
    Property,
    larger_size,
    smaller_size,
)
from css.property import keyword_to_keyword_group_keyword, property_is_inherited
from css.style_values.keyword import KeywordValue
from css.selector_matcher import SelectorMatcher
from css.selector_index import SelectorIndex
from css.stylesheet import CSSStylesheet
from css.style_rule import StyleRule
from css.parser import CSSSyntaxParser
from css.parse_context import ParseContext
from css.initial_value_cache import property_initial_value
from log import log, set_debug, warn

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
        vw: int,
        vh: int,
        preferred_font_size: int = 16,
    ):
        self.selector_index = SelectorIndex()
        self.selector_matcher = SelectorMatcher(history_manager)
        self.stylesheets = stylesheets
        self.vw = vw
        self.vh = vh
        self.DOM = DOM
        self.preferred_font_size = preferred_font_size

    # ================================= Primary Methods ================================= #

    def style_tree(self) -> None:
        # build our index
        for stylesheet in self.stylesheets:
            self.selector_index.build_index_for_rules(stylesheet.rules)

        # recursively style nodes
        def recurse(node: Node):
            log("Styling:", node)
            # filter, match, cascade
            self.match_and_cascade(node)

            # defaulting
            self.compute_defaults(node)

            # resolving
            self.absolutize_values(node)

            for child in node.children:
                recurse(child)

        recurse(self.DOM.document_element)

    def match_and_cascade(self, node: Node) -> None:
        """For an element in the DOM, produce a list of candidate rules through selector matching.
        Then, iterate through rules (in cascade order), applying **specified** properties to the node with tiebreakers.
        """
        if not isinstance(node, Element):
            return

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
                node.specified_style[decl.prop] = decl.val

        # second pass:
        candidate_rules.sort(key=lambda m: m.get_sort_key(important=True))
        for rule in candidate_rules:
            for decl in rule.declarations:
                if not decl.important:
                    continue
                node.specified_style[decl.prop] = decl.val

    def compute_defaults(self, node: Node) -> None:
        """Compute inherited and initial properties"""
        # TODO: provide lazy compute method
        for prop in Property:
            if val := node.specified_style.get(prop):
                if isinstance(val, KeywordValue) and val.is_css_wide():
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

                # if here, node already has prop in specified values, do nothing

            elif property_is_inherited(prop):
                self.inherit_property(node, prop)
            else:
                self.initial_property(node, prop)

    # https://drafts.csswg.org/css-cascade-5/#computed
    def absolutize_values(self, node: Node):
        """
        Absolutize the following values IN ORDER, converting from **specified** to **computed** property
        - TODO: custom idents (var(--hello))
        - font-family/font-size
        - values with relative units (em, ex, vh, vw)
        - smaller, bolder keywords
        - percentage values on line-height
        - relative URLs
        """

        # TODO: custom ident

        # compute font first
        self.compute_font(node)

    # ============================== Compute Default Helpers ============================== #

    def inherit_property(self, node: Node, prop: Property) -> None:
        if node.parent and (val := node.parent.computed_style.get(prop)):
            node.specified_style[prop] = val
        elif not node.parent:
            self.initial_property(node, prop)

    # TODO: finish property/value parser so this doesn't immediately crash everything
    def initial_property(self, node: Node, prop: Property) -> None:
        # log("Initial value for", prop, end=": ")
        init = property_initial_value(prop)
        if init:
            node.specified_style[prop] = init
        # log(init)

    # ============================== Absolutize Value Helpers ============================== #

    def compute_font(self, node: Node) -> None:
        assert node.specified_style.get(Property.FONT_FAMILY)
        assert node.specified_style.get(Property.FONT_SIZE)

        style = node.computed_style.styles

        font_size = style[Property.FONT_SIZE] = self.compute_font_size(node)
        font_weight = style[Property.FONT_WEIGHT] = self.compute_font_weight(node)
        style[Property.FONT_WIDTH] = node.specified_style[Property.FONT_WIDTH]
        font_style = style[Property.FONT_STYLE] = node.specified_style[
            Property.FONT_STYLE
        ]
        style[Property.FONT_VARIATION_SETTINGS] = node.specified_style[
            Property.FONT_VARIATION_SETTINGS
        ]
        style[Property.LINE_HEIGHT] = self.compute_line_height(node)
        style[Property.FONT_FAMILY] = node.specified_style[Property.FONT_FAMILY]

        # generate a tkinter font
        # this technically should be a list, but there's no way to check if a font can display a certain character anyways
        # so fallbacks are not necessary
        families = style[Property.FONT_FAMILY]
        assert isinstance(families, ListStyleValue)
        for font in families.items:
            # font-family = <CustomIdentValue> | <StringValue>
            tk_font_family = "Segoe UI"
            if isinstance(font, CustomIdentValue):
                tk_font_family = font.ident
            elif isinstance(font, StringValue):
                tk_font_family = font.string

            # convert font_size px -> pt for tkinter font
            tk_font_size = int(font_size.length.value * 0.75)
            assert isinstance(font_style, KeywordValue)
            tk_font_style = (
                "italic"
                if font_style.keyword in (Keyword.ITALIC, Keyword.OBLIQUE)
                else "roman"
            )

            if (
                isinstance(font_weight, KeywordValue)
                and font_weight.keyword == Keyword.BOLD
            ):
                tk_font_weight = "bold"
            else:
                tk_font_weight = "normal"

            # verify that tkinter created the right font
            font = get_font(tk_font_family, tk_font_size, tk_font_style, tk_font_weight)
            if font.cget("family").lower() == tk_font_family.lower():
                node.computed_style.font = font
                break

        assert node.computed_style.font

    def compute_font_size(self, node: Node) -> LengthValue:
        """Computes font size pixel value"""
        assert (
            Property.FONT_SIZE in node.specified_style
        ), "Error while absolutizing font size: Font size not found in specified properties"

        specified = node.specified_style[Property.FONT_SIZE]

        # absolutize length unit (rem, em, vh, vw, vi, vb, ex)
        if isinstance(specified, LengthValue) and (
            absolutized := self.absolutize_length(
                node, specified, prop_is_font_size=True
            )
        ):
            return absolutized

        elif isinstance(specified, KeywordValue):
            # is relative size keyword [smaller | larger]
            # compute size against parent, or preferred_font_size if is root node
            if kw := keyword_to_keyword_group_keyword(specified.keyword, RelativeSize):
                if node.parent:
                    parent_size = node.parent.computed_style.get(Property.FONT_SIZE)
                    assert isinstance(parent_size, LengthValue)
                    base_size = parent_size.length.value
                else:
                    base_size = self.preferred_font_size

                if kw == RelativeSize.SMALLER:
                    smaller = smaller_size(base_size=base_size)
                    return LengthValue(Length.from_px(smaller))
                elif kw == RelativeSize.LARGER:
                    larger = larger_size(base_size=base_size)
                    return LengthValue(Length.from_px(larger))

            # is absolute size keyword [x-small, normal, large, xxx-large, etc]
            elif kw := keyword_to_keyword_group_keyword(
                specified.keyword, AbsoluteSize
            ):
                assert isinstance(kw, AbsoluteSize)
                return LengthValue(Length.from_px(FONT_SIZE_SCALING_TABLE[kw]))
            assert False, f"Unrecognized Keyword {specified} for font-size"

        elif isinstance(specified, PercentageValue):
            # resolve to px immediately
            base_px = self._get_base_font_size_px(node, True, not node.parent)
            return LengthValue(Length.from_px(base_px * specified.percentage))

        else:
            # value is already absolute (e.g. font-size: 16px;)
            assert isinstance(specified, LengthValue)
            return LengthValue(specified.length.to_px())

    def _get_base_font_size_px(
        self, node: Node, prop_is_font_size: bool, from_root: bool = False
    ) -> float:
        """Get the base font size in pixels for em/rem calculations."""
        if prop_is_font_size:
            if not node.parent:
                return float(self.preferred_font_size)

            if from_root:
                base_font_size = node.get_root().computed_style.get(Property.FONT_SIZE)
            else:
                base_font_size = node.parent.computed_style.get(Property.FONT_SIZE)
        else:
            # for non-font-size properties, use current node's font size
            base_font_size = node.computed_style.get(Property.FONT_SIZE)

        assert isinstance(base_font_size, LengthValue)
        assert base_font_size.length.unit == LengthUnit.PX
        return base_font_size.length.value

    def compute_font_weight(self, node: Node) -> KeywordValue:
        font_weight = node.specified_style.get(Property.FONT_WEIGHT)
        assert font_weight, "Font weight not found in specified properties"

        if isinstance(font_weight, KeywordValue):
            if font_weight.keyword in (Keyword.BOLD, Keyword.NORMAL):
                return font_weight

        # TODO: number values, Lighter, Bolder (tkinter doesn't support any of these anyways)
        return KeywordValue("normal")

    def compute_line_height(
        self, node: Node
    ) -> KeywordValue | NumberValue | LengthValue:
        specified = node.specified_style[Property.LINE_HEIGHT]
        if isinstance(specified, KeywordValue) and specified.keyword == Keyword.NORMAL:
            return specified

        if isinstance(specified, (NumberValue, LengthValue)):
            return specified

        if isinstance(specified, PercentageValue):
            # by now, font size will have already been computed
            font_size = node.computed_style.get(Property.FONT_SIZE)
            assert isinstance(font_size, LengthValue)
            length = Length.from_px(font_size.raw_value * specified.percentage)
            return LengthValue(length)

        assert False

    def absolutize_length(
        self, node: Node, val: LengthValue, prop_is_font_size: bool = False
    ) -> LengthValue | None:
        """Converts a LengthValue from a **relative** length to an **absolute** length.
        `prop_is_font_size` affects computing for (r)em / ex / viewport values. For example,
        `font-size: 1.5em;` requires inheriting computed font size from parent, whereas
        `border-width: 1.5em;` looks at the current node's computed font-size.

        Units include: rem, em, ex, cap, ch, ic, ih, ...
        """
        unit = val.length.unit
        value = val.length.value

        if unit == LengthUnit.PX:
            return val

        # EM and REM units
        if unit == LengthUnit.EM:
            base_px = self._get_base_font_size_px(
                node, prop_is_font_size, from_root=False
            )
            return LengthValue(Length.from_px(base_px * value))

        if unit == LengthUnit.REM:
            base_px = self._get_base_font_size_px(
                node, prop_is_font_size, from_root=True
            )
            return LengthValue(Length.from_px(base_px * value))

        # viewport units
        if unit == LengthUnit.VW or unit == LengthUnit.VI:
            # TODO: writing direction context so VI/VB actually work
            px = self.vw * value
            return LengthValue(Length.from_px(px))

        if unit == LengthUnit.VH or unit == LengthUnit.VB:
            px = self.vh * value
            return LengthValue(Length.from_px(px))

        # TODO: other relative units
        warn(f"{unit} needs to be implemented")
        return None

    def print_tree(self, prop: Property | None = None) -> None:
        def recurse(node: Node):
            if isinstance(node, Element):
                log(f"{node.tag}:")
            elif isinstance(node, Text):
                log(f"'{node.text}':")

            for key, val in node.computed_style.styles.items():
                if not prop or key == prop:
                    log(f"    {key.value} = {val};")

            for child in node.children:
                recurse(child)

        recurse(self.DOM.document_element)


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()

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
                <p id="p">p_inside</p>
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
        font-size: 33px;
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
    print("Styling:")
    computer = StyleComputer(doc, [stylesheet, stylesheet2], history, vw=800, vh=600)
    computer.style_tree()
    computer.print_tree()
