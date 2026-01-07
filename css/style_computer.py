import css.property
import css.property
import css.property
import css.property
from operator import is_
from css.property import property_is_shorthand
from css.style_values.shorthand import ShorthandStyleValue
from dom import Document, Node, Element, Text
from font_cache import get_font
from history import HistoryManager
from css.style_values.numeric import NumberValue
from css.style_values.string import StringValue
from css.style_values.custom_ident import CustomIdentValue
from css.style_values.list import ListStyleValue
from css.style_values.dimension import PercentageValue, Length, LengthValue
from css.style_values.keyword import KeywordValue
from css.units import LengthUnit
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
from css.selector_matcher import SelectorMatcher
from css.selector_index import SelectorIndex
from css.stylesheet import CSSStylesheet
from css.style_rule import StyleRule
from css.parser import CSSSyntaxParser
from css.parse_context import ParseContext
from css.initial_value_cache import property_initial_value
from log import log, set_debug
from css.style_values.dimension import FontMetrics, LengthResolutionContext
from css.compute_context import ComputeContext

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
            self.absolutize_properties(node)

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
        def apply_candidate_rules(rules: list[StyleRule], important: bool):
            for rule in rules:
                for decl in rule.declarations:
                    # skip important decls when important=True
                    if decl.important ^ important:
                        continue

                    node.specified_style[decl.prop] = decl.val

                    # expand shorthand properties
                    # FIXME: since I've only implemented the `font` property,
                    # I'm expecting a ShorthandStyleValue. This may not be true for other shorthands.
                    if isinstance(decl.val, ShorthandStyleValue):
                        for prop, val in decl.val.sub_properties.items():
                            node.specified_style[prop] = val

        # first pass:
        # sort rules by cascade order (origin, specificity, then source order) in ascending order
        candidate_rules.sort(key=lambda m: m.get_sort_key(important=False))
        apply_candidate_rules(candidate_rules, important=False)

        # second pass:
        candidate_rules.sort(key=lambda m: m.get_sort_key(important=True))
        apply_candidate_rules(candidate_rules, important=True)

    def compute_defaults(self, node: Node) -> None:
        """Compute inherited and initial properties"""
        # TODO: provide lazy compute method
        for prop in Property:

            # only longhands should be stored on nodes
            if property_is_shorthand(prop) or prop == Property.CUSTOM:
                continue

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
    def absolutize_properties(self, node: Node):
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

        # create computation context to compute length
        # if is root node, use default font metrics (size 16, 22)
        default_font_metrics = FontMetrics(
            self.preferred_font_size, self.preferred_font_size * 1.375
        )
        computation_context = ComputeContext(
            length_context=(
                LengthResolutionContext.for_element(node.parent, self.vw, self.vh)
                if node.parent
                else LengthResolutionContext(
                    vw=self.vw,
                    vh=self.vh,
                    font_metrics=default_font_metrics,
                    root_font_metrics=default_font_metrics,
                )
            )
        )

        # compute font first
        self.compute_font(node, computation_context)

        # compute rest of property values
        for prop, style in node.specified_style.items():
            # if property is already computed, we can skip over them
            if node.computed_style.get(prop):
                continue

            # TODO: do special processing for some properties
            # checkout lb StyleComputer.cpp StyleComputer::compute_value_of_property

            node.computed_style.styles[prop] = style.absolutize(computation_context)

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

    def compute_font(self, node: Node, computation_context: ComputeContext) -> None:
        assert node.specified_style.get(Property.FONT_FAMILY)
        assert node.specified_style.get(Property.FONT_SIZE)

        style = node.computed_style.styles

        font_size = style[Property.FONT_SIZE] = self.compute_font_size(
            node, computation_context
        )
        font_weight = style[Property.FONT_WEIGHT] = self.compute_font_weight(node)
        style[Property.FONT_WIDTH] = node.specified_style[Property.FONT_WIDTH]
        font_style = style[Property.FONT_STYLE] = node.specified_style[
            Property.FONT_STYLE
        ]
        style[Property.FONT_VARIATION_SETTINGS] = node.specified_style[
            Property.FONT_VARIATION_SETTINGS
        ]
        style[Property.LINE_HEIGHT] = self.compute_line_height(
            node, computation_context
        )
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

    def compute_font_size(
        self, node: Node, computation_context: ComputeContext
    ) -> LengthValue:
        """Computes font size pixel value"""
        assert (
            Property.FONT_SIZE in node.specified_style
        ), "Error while absolutizing font size: Font size not found in specified properties"

        specified = node.specified_style[Property.FONT_SIZE].absolutize(
            computation_context
        )

        # LengthValue absolutized to px
        if isinstance(specified, LengthValue):
            assert specified.length.unit == LengthUnit.PX, "must be absolutized to px"
            return specified

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
        self, node: Node, computation_context: ComputeContext
    ) -> KeywordValue | NumberValue | LengthValue:

        specified = node.specified_style[Property.LINE_HEIGHT].absolutize(
            computation_context
        )

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

    def print_tree(self, prop: list[Property] | None = None) -> None:
        def recurse(node: Node):
            if isinstance(node, Element):
                log(f"{node.tag}:")
            if isinstance(node, Text):
                log(f"'{node.text}':")

            for key, val in node.computed_style.styles.items():
                if not prop or key in prop:
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
            <pre style="text-wrap-mode: nowrap;"> hello </pre>
        </body>
    </html>
    """
    with open("css/browser.css", "r") as f:
        browser_css = f.read()

    user_css = """
    body h1 {
        color: red !important;
        font: normal normal bold smaller/1.5 "Arial";
    }

    div.test{
        color: orange !important;
        font-size: 1lh;
        line-height: 1em;
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
    computer.print_tree(
        prop=[
            Property.WHITE_SPACE_COLLAPSE,
            Property.TEXT_WRAP_MODE,
            Property.WHITE_SPACE_TRIM,
        ]
    )
