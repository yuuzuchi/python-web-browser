from css.style_values.dimension import TimeValue
from css.style_values.dimension import AngleValue
from css.style_values.dimension import LengthValue
from css.style_values.dimension import PercentageValue
from css.style_values.calculated import CalculatedValue
from css.style_values.custom_ident import CustomIdentValue
from css.style_values.string import StringValue
from css.style_values.shorthand import ShorthandStyleValue
from css.style_values.keyword import KeywordValue
from css.style_values.list import ListStyleValue
from css.style_values.base import StyleValue
from css.enums import Property, Keyword
from typing import Callable
from css.components import Component
from css.parser import Declaration
from css.value_parser import ValueParser
from css.property import *
from css.lexer import Lexer, Token, Tok
from css.token_stream import CSSTokenStream
from css.initial_value_cache import property_initial_value
from log import log, err, set_debug


GENERIC_FONT_FAMILIES = [
    "serif",
    "sans-serif",
    "cursive",
    "fantasy",
    "monospace",
    "math",
    "ui-serif",
    "ui-sans-serif",
    "ui-monospace",
    "ui-rounded",
]

VALUE_TYPE_PRECEDENCE = [
    ValueType.COLOR,
    ValueType.CORNER_SHAPE,
    ValueType.COUNTER,
    ValueType.DASHED_IDENT,
    ValueType.EASING_FUNCTION,
    ValueType.IMAGE,
    ValueType.POSITION,
    ValueType.BACKGROUND_POSITION,
    ValueType.BASIC_SHAPE,
    ValueType.RATIO,
    ValueType.OPACITY,
    ValueType.OPENTYPE_TAG,
    ValueType.RECT,
    ValueType.STRING,
    ValueType.TRANSFORM_FUNCTION,
    ValueType.TRANSFORM_LIST,
    ValueType.URL,
    ValueType.INTEGER,
    ValueType.NUMBER,
    ValueType.ANGLE,
    ValueType.FLEX,
    ValueType.FREQUENCY,
    ValueType.FIT_CONTENT,
    ValueType.RESOLUTION,
    ValueType.TIME,
    ValueType.PERCENTAGE,
    ValueType.PAINT,
    ValueType.ANCHOR,
]

SIMPLE_TYPES = VALUE_TYPE_PRECEDENCE[:16]


# https://www.w3.org/TR/css-values-4/
class PropertyParser:
    def __init__(self, inp):
        self.stream = inp
        if not isinstance(inp, CSSTokenStream):
            self.stream = CSSTokenStream(inp)
        self.value_parser = ValueParser(self.stream)

    def parse_entire_value(self, property: Property) -> StyleValue | None:
        """
        Parses a full declaration. Used as the primary entry point.
        1. If value is a CSS-wide/builtin ident, parse and return.
        2. Return UnresolvedStyleValue if value is a custom property (e.g. --foo), or value must be computed/substituted at runtime
        3. Dispatch to property-specific parsers for complex grammars (font, background, etc)
        4. Parse positional value list shorthand properties (margin: 0 0 10px 10px)
        5. Parse single-property value lists (font-weight, box-shadow, etc)
        6. Parse multi-property value lists aka shorthands (e.g. border)
        6.1. If shorthand, supply initial values to unspecified sub-properties
        """

        # TODO: check substitution preference of entire value

        # helper to parse entire value. Takes a parse function as input, e.g. parse_as(self.parse_font_style)
        def parse_as(callback: Callable) -> StyleValue | None:
            self.stream.consume_whitespace()
            parsed = callback()
            self.stream.consume_whitespace()
            if parsed and not self.stream.has_next():
                return parsed
            return None

        # 1. parse builtin
        res = parse_as(self.parse_builtin_value)
        if isinstance(res, StyleValue):
            return res

        # TODO 2. return unresolved style value for substituted values
        self.stream.consume_whitespace()
        if not self.stream.has_next():
            return self.parse_error("Error parsing value: Early EOF")

        # 3. dispatch to property-specific parsers
        match property:
            case Property.FONT:
                return parse_as(self.parse_font_value)
            case Property.FONT_FAMILY:
                return parse_as(self.parse_font_family_value)
            case Property.FONT_VARIANT:
                return parse_as(self.parse_font_variant_value)

        # 4. dispatch positional value list shorthands (margin, inset, border-radius, etc)
        if property_is_positional_value_list_shorthand(property):
            res = self.parse_positional_value_list_shorthand(property)
            if res and not self.stream.has_next():
                return res
            return self.parse_error("Failed to parse positional value list shorthand")

        # 5. single-property value lists
        with self.stream.transaction() as tx:
            parsed = []
            while True:
                self.stream.consume_whitespace()
                if not self.stream.has_next():
                    break

                res = self.parse_value_for_property(property)
                if not res:
                    break
                parsed.append(res)

            self.stream.consume_whitespace()
            if not self.stream.has_next():
                tx.commit()
                if len(parsed) == 1:
                    return parsed[0]
                return ListStyleValue(parsed, delim=" ")

    # ======================== Parser Helper Functions ======================== #

    def parse_error(self, msg) -> None:
        err(msg)

    # hook for parsing comma separated list
    # parses each item with input function parse_func
    def parse_comma_separated_value_list(
        self,
        parse_func: Callable,
    ) -> ListStyleValue | None:
        self.stream.consume_whitespace()
        first = parse_func()
        self.stream.consume_whitespace()

        if not first or self.stream.peek().type == Tok.EOF:
            return ListStyleValue([first], delim=",")

        values = [first]
        while self.stream.peek().type != Tok.EOF:
            if self.stream.consume().type != Tok.COMMA:
                return None

            self.stream.consume_whitespace()
            res = parse_func()
            if res:
                values.append(res)
                self.stream.consume_whitespace()
            else:
                return None
        return ListStyleValue(values, delim=",")

    def parse_positional_value_list_shorthand(self, property: Property) -> StyleValue:
        pass

    def parse_value_for_property(self, property: Property) -> StyleValue | None:
        """
        Attempt to parse a single value (a token) for a property.
        First checks if the token is a keyword, and if the property accepts the keyword.
        Then checks if property accepts any of the ValueTypes, and if so, parses the token against that ValueType.
        Called by parse_value from step 5.
        """
        self.stream.consume_whitespace()
        tok = self.stream.peek()

        # does property accept a parsed keyword?
        if tok.type == Tok.IDENT and tok.val and tok.val in Keyword:
            keyword = KeywordValue(tok.val)
            if not keyword.is_css_wide() and property_accepts_keyword(
                property, Keyword(tok.val)
            ):
                self.stream.consume()
                return keyword

        if not (accepted_types := property_accepted_types(property)):
            err(f"{property} accepts no value types!")
            return

        for t in VALUE_TYPE_PRECEDENCE:
            if t not in accepted_types:
                continue

            if t in SIMPLE_TYPES:
                # self.value_parser.set_context(self.stream, t)
                if value := self.value_parser.parse(t):
                    return value

            # range check, and integer/number comes before length (0 should be int/number if both allowed)
            elif t == ValueType.INTEGER:
                # self.value_parser.set_context(self.e
                if value := self.value_parser.parse_integer_value():
                    if property_accepts_integer(property, value.int_value):
                        return value

            elif t == ValueType.NUMBER:
                # self.value_parser.set_context(self.stream, t)
                with self.stream.transaction() as tx:
                    if value := self.value_parser.parse_number_value():
                        if property_accepts_number(property, value.num_value):
                            tx.commit()
                            return value

            elif t == ValueType.ANGLE:
                with self.stream.transaction() as tx:
                    if ValueType.PERCENTAGE in accepted_types:
                        # self.value_parser.set_context(
                        #     self.stream, ValueType.ANGLE_PERCENTAGE
                        # )
                        if value := self.value_parser.parse_angle_percentage_value():
                            # fmt: off
                            if isinstance(value, CalculatedValue) or (
                                isinstance(value, AngleValue) and property_accepts_angle(property, value.to_degrees())) or (
                                isinstance(value, PercentageValue) and property_accepts_percentage(property, value.percentage)
                            ):  # fmt: on
                                tx.commit()
                                return value

                    if value := self.value_parser.parse_angle_value():
                        if isinstance(value, CalculatedValue) or (
                            isinstance(value, AngleValue)
                            and property_accepts_angle(property, value.to_degrees())
                        ):
                            tx.commit()
                            return value

            elif t == ValueType.FLEX:
                # self.value_parser.set_context(self.stream, t)
                with self.stream.transaction() as tx:
                    if value := self.value_parser.parse_flex_value():
                        if isinstance(value, CalculatedValue):
                            # or (
                            #     isinstance(value, FlexValue)
                            #     and property_accepts_flex(property, value.flex)
                            # )
                            # no properties accept flex value type
                            tx.commit()
                            return value

            elif t == ValueType.FREQUENCY:
                with self.stream.transaction() as tx:
                    if ValueType.PERCENTAGE in accepted_types:
                        # self.value_parser.set_context(
                        #     self.stream, ValueType.FREQUENCY_PERCENTAGE
                        # )
                        if (
                            value := self.value_parser.parse_frequency_percentage_value()
                        ):
                            # fmt: off
                            if isinstance(value, CalculatedValue) or (
                                #isinstance(value, FrequencyValue) and property_accepts_frequency(property, value.frequency)) or (
                                isinstance(value, PercentageValue) and property_accepts_percentage(property, value.percentage)
                            ):  # fmt: on
                                tx.commit()
                                return value

                    if value := self.value_parser.parse_frequency_value():
                        if isinstance(value, CalculatedValue):  # or (
                            # isinstance(value, FrequencyValue)
                            # and property_accepts_frequency(property, value.frequency)
                            # ):
                            tx.commit()
                            return value

            elif t == ValueType.FIT_CONTENT:
                if value := self.value_parser.parse_fit_content_value():
                    return value

            elif t == ValueType.LENGTH:
                with self.stream.transaction() as tx:
                    if ValueType.PERCENTAGE in accepted_types:
                        # self.value_parser.set_context(
                        #     self.stream, ValueType.LENGTH_PERCENTAGE
                        # )
                        if value := self.value_parser.parse_length_percentage_value():
                            # fmt: off
                            if isinstance(value, CalculatedValue) or (
                                isinstance(value, LengthValue) and property_accepts_length(property, value.length.value)) or (
                                isinstance(value, PercentageValue) and property_accepts_percentage(property, value.percentage)
                            ):  # fmt: on
                                tx.commit()
                                return value

                    if value := self.value_parser.parse_length_value():
                        if isinstance(value, CalculatedValue) or (
                            isinstance(value, LengthValue)
                            and property_accepts_length(property, value.length.value)
                        ):
                            tx.commit()
                            return value

            elif t == ValueType.RESOLUTION:
                # self.value_parser.set_context(self.stream, t)
                with self.stream.transaction() as tx:
                    if value := self.value_parser.parse_resolution_value():
                        if isinstance(value, CalculatedValue):  # or (
                            #     isinstance(value, ResolutionValue)
                            #     and property_accepts_resolution(property, value.resolution)
                            # ):
                            tx.commit()
                            return value

            elif t == ValueType.TIME:
                with self.stream.transaction() as tx:
                    if ValueType.PERCENTAGE in accepted_types:
                        # self.value_parser.set_context(
                        #     self.stream, ValueType.LENGTH_PERCENTAGE
                        # )
                        if value := self.value_parser.parse_time_percentage_value():
                            # fmt: off
                            if isinstance(value, CalculatedValue) or (
                                isinstance(value, TimeValue) and property_accepts_time(property, value.time)) or (
                                isinstance(value, PercentageValue) and property_accepts_percentage(property, value.percentage)
                            ):  # fmt: on
                                tx.commit()
                                return value

                    if value := self.value_parser.parse_time_value():
                        if isinstance(value, CalculatedValue) or (
                            isinstance(value, TimeValue)
                            and property_accepts_time(property, value.time)
                        ):
                            tx.commit()
                            return value

            elif t == ValueType.PERCENTAGE:
                # self.value_parser.set_context(self.stream, t)
                with self.stream.transaction() as tx:
                    if value := self.value_parser.parse_percentage_value():
                        if isinstance(value, CalculatedValue) or (
                            isinstance(value, PercentageValue)
                            and property_accepts_percentage(property, value.percentage)
                        ):
                            tx.commit()
                            return value

            elif t == ValueType.PAINT:
                if value := self.value_parser.parse_paint_value():
                    return value

            elif t == ValueType.ANCHOR:
                if value := self.value_parser.parse_anchor_value():
                    return value

            return None

    def parse_value_for_properties(
        self, properties: list[Property]
    ) -> tuple[Property, StyleValue] | None:
        # greedily parse value for each property
        for property in properties:
            if value := self.parse_value_for_property(property):
                return property, value
        return None

    # ================================ Textual ================================ #

    def parse_builtin_value(self) -> KeywordValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.IDENT and tok.val:
            if tok.val in Keyword:
                keyword = KeywordValue(tok.val)
                if keyword.is_css_wide():
                    self.stream.consume()  # ident
                    return keyword

    # ================================= Fonts ================================= #

    # [ [ <'font-style'> || <font-variant-css2> || <'font-weight'> || <font-width-css3> ]? <'font-size'> [ / <'line-height'> ]? <'font-family'># ] | <system-family-name>
    def parse_font_value(self) -> ShorthandStyleValue | None:
        font_style = font_variant = font_weight = font_width = font_size = line_height = font_family = None # fmt: skip

        self.stream.consume_whitespace()
        while self.stream.has_next():
            # <font-variant-css2> = normal | small-caps
            # <font-width-css3> = normal | ultra-condensed | extra-condensed | condensed | semi-condensed | semi-expanded | expanded | extra-expanded | ultra-expanded
            tok = self.stream.peek()
            if tok.is_ident("normal"):
                self.stream.consume()
                self.stream.consume_whitespace()
                continue

            # font-size is MANDATORY, so once we seem a dim (not angle), we know what comes after must be /<line-height>? <font-family>
            # <font-size> = <absolute-size> | <relative-size> | <length-percentage [0,∞]> | math
            elif font_size := self.parse_value_for_property(Property.FONT_SIZE):
                self.stream.consume_whitespace()
                break

            # font style: normal | italic | oblique <angle [-90deg,90deg]>?
            elif not font_style and (tok.is_ident("italic") or tok.is_ident("oblique")):
                font_style = self.parse_value_for_property(Property.FONT_STYLE)
                self.stream.consume_whitespace()
                continue

            # <font-variant-css2> = normal | small-caps
            elif not font_variant and tok.is_ident("small-caps"):
                self.stream.consume()
                # fmt: off
                font_variant = ShorthandStyleValue(Property.FONT_VARIANT, {
                    Property.FONT_VARIANT_CAPS:             property_initial_value(Property.FONT_VARIANT_ALTERNATES),
                    Property.FONT_VARIANT_EAST_ASIAN:       KeywordValue("small-caps"),
                    Property.FONT_VARIANT_EMOJI:            property_initial_value(Property.FONT_VARIANT_EMOJI),
                    Property.FONT_VARIANT_LIGATURES:        property_initial_value(Property.FONT_VARIANT_LIGATURES),
                    Property.FONT_VARIANT_NUMERIC:          property_initial_value(Property.FONT_VARIANT_NUMERIC),
                    Property.FONT_VARIANT_POSITION:         property_initial_value(Property.FONT_VARIANT_POSITION)
                })  # fmt: on
                self.stream.consume_whitespace()
                continue

            # <font-weight> = <font-weight-absolute> | bolder | lighter
            elif not font_weight and (
                tok.type == Tok.NUMBER
                or tok.is_ident("bold")
                or tok.is_ident("bolder")
                or tok.is_ident("lighter")
            ):
                font_weight = self.parse_value_for_property(Property.FONT_WEIGHT)
                self.stream.consume_whitespace()
                continue

            # <font-width-css3> = normal | ultra-condensed | extra-condensed | condensed | semi-condensed | semi-expanded | expanded | extra-expanded | ultra-expanded
            elif not font_width and tok.type == Tok.IDENT:
                with self.stream.transaction() as tx:
                    keyword = KeywordValue(self.stream.consume().val)
                    self.stream.consume_whitespace()
                    if keyword.keyword in (Keyword.ULTRA_CONDENSED, Keyword.EXTRA_CONDENSED, Keyword.CONDENSED, Keyword.SEMI_CONDENSED, Keyword.SEMI_EXPANDED, Keyword.EXPANDED, Keyword.EXTRA_EXPANDED, Keyword.ULTRA_EXPANDED): # fmt: skip
                        font_width = keyword
                        tx.commit()
                        continue

            else:
                break

        if not font_size:
            return self.parse_error(
                "Error parsing property `font`: expected sub-property font-size"
            )

        self.stream.consume_whitespace()
        if self.stream.peek().is_delim("/"):
            self.stream.consume()
            line_height = self.parse_value_for_property(Property.LINE_HEIGHT)

        self.stream.consume_whitespace()
        self.stream.peek()
        font_family = self.parse_font_family_value()

        if not font_family:
            return self.parse_error(
                "Error parsing property `font`: expected last sub-property font-family"
            )

        # fill in any missing sub properties
        if not font_style:
            font_style = property_initial_value(Property.FONT_STYLE)
        if not font_variant:
            font_variant = property_initial_value(Property.FONT_VARIANT)
        if not font_weight:
            font_weight = property_initial_value(Property.FONT_WEIGHT)
        if not font_width:
            font_width = property_initial_value(Property.FONT_WIDTH)
        if not line_height:
            line_height = property_initial_value(Property.LINE_HEIGHT)

        # fmt: off
        return ShorthandStyleValue(Property.FONT, { 
            Property.FONT_FAMILY: font_family,
            Property.FONT_SIZE: font_size,
            Property.FONT_WIDTH: font_width,
            Property.FONT_STYLE: font_style,
            Property.FONT_VARIANT: font_variant,
            Property.FONT_WEIGHT: font_weight,
            Property.LINE_HEIGHT: line_height,
            Property.FONT_FEATURE_SETTINGS: KeywordValue("initial"),
            Property.FONT_KERNING: property_initial_value(Property.FONT_KERNING),
            Property.FONT_LANGUAGE_OVERRIDE: KeywordValue("initial"),
            Property.FONT_VARIATION_SETTINGS: KeywordValue("initial")
        })  # fmt: on

    # [ <family-name> | <generic-family> ]#
    def parse_font_family_value(
        self,
    ) -> ListStyleValue | CustomIdentValue | StringValue | None:

        def parse_a_value() -> CustomIdentValue | StringValue | None:
            self.stream.consume_whitespace()

            # gerneric family cannot be quoted, so we'll check for ident first
            tok = self.stream.peek()
            if tok.type == Tok.IDENT and tok.val.lower() in GENERIC_FONT_FAMILIES:
                font = self.stream.consume()
                self.stream.consume_whitespace()
                return CustomIdentValue(font.val)
            # <family-name>
            else:
                return self.parse_family_name_value()

        return self.parse_comma_separated_value_list(parse_a_value)

    # <family-name> = <string> | <custom-ident>+
    def parse_family_name_value(self) -> StringValue | CustomIdentValue | None:
        self.stream.consume_whitespace()
        parts = []
        while self.stream.peek().type != Tok.EOF:
            tok = self.stream.peek()

            if tok.type == Tok.STRING:
                if parts:  # string must be first item
                    return self.parse_error(
                        "Error while parsing font family name value: quoted family name must come first"
                    )
                self.stream.consume()
                self.stream.consume_whitespace()
                return StringValue(tok.val)

            if tok.type == Tok.IDENT:
                parts.append(self.stream.consume().val)
                self.stream.consume_whitespace()
                continue
            break

        if not parts:
            return

        if len(parts) == 1:
            # no generic fonts allowed
            part = parts[0]
            if KeywordValue(part).is_css_wide():
                return self.parse_error(
                    "Error while parsing font family name value: font family is a generic family"
                )

            if part in GENERIC_FONT_FAMILIES:
                return self.parse_error(
                    "Error while parsing font family name value: font family is a generic family"
                )

        return CustomIdentValue(" ".join(parts))

    # https://drafts.csswg.org/css-fonts/#propdef-font-variant
    # TODO: yeah no
    # normal | none |
    # [ [ <common-lig-values> || <discretionary-lig-values> || <historical-lig-values> || <contextual-alt-values> ]
    # || [ small-caps | all-small-caps | petite-caps | all-petite-caps | unicase | titling-caps ] ||
    # [ FIXME: stylistic(<feature-value-name>) ||
    # historical-forms ||
    # FIXME: styleset(<feature-value-name>#) ||
    # FIXME: character-variant(<feature-value-name>#) ||
    # FIXME: swash(<feature-value-name>) ||
    # FIXME: ornaments(<feature-value-name>) ||
    # FIXME: annotation(<feature-value-name>) ] ||
    # [ <numeric-figure-values> || <numeric-spacing-values> || <numeric-fraction-values> ||
    # ordinal || slashed-zero ] || [ <east-asian-variant-values> || <east-asian-width-values> || ruby ] ||
    # [ sub | super ] || [ text | emoji | unicode ] ]
    def parse_font_variant_value(self):
        self.stream.consume()
        self.stream.consume_whitespace()
        return KeywordValue("normal")


if __name__ == "__main__":
    set_debug()
    declaration = """
    
    font: normal normal bold small/1.5 "Arial";
    /*font-style: normal;*/
    
    """
    toks = Lexer(declaration).parse()
    from css.parser import CSSSyntaxParser

    contents = CSSSyntaxParser().parse_declaration_list(toks)
    prop = Property.from_name(contents[0].name)
    val = contents[0].val
    log("Input token stream:", val)
    log("Declaration:", contents)
    parser = PropertyParser(val)
    out = parser.parse_entire_value(prop)
    log("\nOutput Style Value:", out)

    # initial = parser.property_initial_value(prop)
    # log(f"Initial value for {prop}: {initial}")
