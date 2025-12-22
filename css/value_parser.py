from css.style_values.dimension import Length
from css.units import LengthUnit
from css.lexer import Num
from css.style_values.custom_ident import CustomIdentValue
from css.style_values.base import StyleValue
from css.style_values.keyword import KeywordValue
from css.style_values.numeric import NumberValue, IntegerValue
from css.style_values.string import StringValue
from css.style_values.url import URLValue
from css.style_values.color import Color, ColorValue
from css.style_values.shape import BasicShapeValue, BasicShape
from css.style_values.dimension import (
    PercentageValue,
    TimeValue,
    AngleValue,
    LengthValue,
)
from css.style_values.anchor import AnchorSizeValue, AnchorValue
from css.lexer import Tok
from css.components import Function
from css.property import keyword_to_keyword_group_keyword
from css.token_stream import CSSTokenStream
from css.enums import Property, ValueType, Keyword
import css.enums as enums


class ValueParser:

    def __init__(self, inp: list | CSSTokenStream):
        if not isinstance(inp, CSSTokenStream):
            self.stream = CSSTokenStream(inp)
        else:
            self.stream = inp

    def set_context(self, property: Property):
        self.property = property

    def parse(self, type: ValueType) -> StyleValue | None:
        print(f"parse: {type}")
        match type:
            case ValueType.ANCHOR:
                return self.parse_anchor_value()
            case ValueType.ANCHOR_SIZE:
                return self.parse_anchor_size()
            case ValueType.ANGLE:
                return self.parse_angle_value()
            case ValueType.ANGLE_PERCENTAGE:
                return self.parse_angle_percentage_value()
            # case ValueType.BACKGROUND_POSITION:
            #     return self.parse_position_value(ValueType.BACKGROUND_POSITION)
            case ValueType.BASIC_SHAPE:
                return self.parse_basic_shape_value()
            case ValueType.COLOR:
                return self.parse_color_value()
            # case ValueType.CORNER_SHAPE:
            #     return self.parse_corner_shape_value()
            # case ValueType.COUNTER:
            #     return self.parse_counter_value()
            case ValueType.CUSTOM_IDENT:
                return self.parse_custom_ident_value(blacklist=[])
            case ValueType.DASHED_IDENT:
                return self.parse_dashed_ident_value()
            # case ValueType.EASING_FUNCTION:
            #     return self.parse_easing_value()
            # case ValueType.FILTER_VALUE_LIST:
            #     return self.parse_filter_value_list_value()
            # case ValueType.FIT_CONTENT:
            #     return self.parse_fit_content_value()
            # case ValueType.FLEX:
            #     return self.parse_flex_value()
            # case ValueType.FREQUENCY:
            #     return self.parse_frequency_value()
            # case ValueType.FREQUENCY_PERCENTAGE:
            #     return self.parse_frequency_percentage_value()
            # case ValueType.IMAGE:
            #     return self.parse_image_value()
            case ValueType.INTEGER:
                return self.parse_integer_value()
            case ValueType.LENGTH:
                return self.parse_length_value()
            case ValueType.LENGTH_PERCENTAGE:
                return self.parse_length_percentage_value()
            case ValueType.NUMBER:
                return self.parse_number_value()
            # case ValueType.OPACITY:
            #     return self.parse_opacity_value()
            # case ValueType.OPENTYPE_TAG:
            #     return self.parse_opentype_tag_value()
            # case ValueType.PAINT:
            #     return self.parse_paint_value()
            case ValueType.PERCENTAGE:
                return self.parse_percentage_value()
            # case ValueType.POSITION:
            #     return self.parse_position_value()
            # case ValueType.RATIO:
            #     return self.parse_ratio_value()
            # case ValueType.RECT:
            #     return self.parse_rect_value()
            # case ValueType.RESOLUTION:
            #     return self.parse_resolution_value()
            case ValueType.STRING:
                return self.parse_string_value()
            # case ValueType.TIME:
            #     return self.parse_time_value()
            # case ValueType.TIME_PERCENTAGE:
            #     return self.parse_time_percentage_value()
            # case ValueType.TRANSFORM_FUNCTION:
            #     return self.parse_transform_function_value()
            # case ValueType.TRANSFORM_LIST:
            #     return self.parse_transform_list_value()
            # case ValueType.URL:
            #     return self.parse_url_value()
            case _:
                # err("nonexistant value type")
                raise AssertionError("nonexistant value type")

    def parse_keyword_value(self) -> KeywordValue | None:
        keyword = self.stream.peek()
        if keyword.type == Tok.IDENT and keyword.val in Keyword:
            self.stream.consume()
            return KeywordValue(str(keyword.val))

    # https://drafts.csswg.org/css-anchor-position-1/#anchor-pos
    def parse_anchor_value(self) -> AnchorValue | None:
        # anchor( <anchor-name>? && <anchor-side>, <length-percentage>? )
        with self.stream.transaction() as tx:
            func_tok = self.stream.consume()
            if not isinstance(func_tok, Function) or func_tok.name != "anchor":
                return

            anchor_name = ""
            anchor_side = None
            fallback = None

            for _ in range(2):
                # <anchor-name> = <dashed-ident>
                if dashed_ident := self.parse_dashed_ident():
                    if anchor_name:
                        return

                    anchor_name = dashed_ident

                # <anchor_side> = inside | outside | top | left | right | bottom
                #   | start | end | self-start | self-end | <percentage> | center
                anchor_side = self.parse_keyword_value()
                if not anchor_side:
                    # must be <percentage>, parse <length-percentage> and throw out any length values to handle calc
                    # ex: anchor(calc(10% + 20%)) is allowed, but anchor(calc(10% + 20px)) is not
                    anchor_side = self.parse_length_percentage_value()
                    if not anchor_side or isinstance(anchor_side, LengthValue):
                        return

                elif not keyword_to_keyword_group_keyword(
                    anchor_side.keyword, enums.AnchorSide
                ):
                    return

            if self.stream.peek().type == Tok.COMMA:
                self.stream.consume()
                self.stream.consume_whitespace()
                if not (fallback := self.parse_length_percentage_value()):
                    return

            if anchor_side and not self.stream.has_next():
                tx.commit()
                return AnchorValue(anchor_name, anchor_side, fallback)

    # https://drafts.csswg.org/css-anchor-position-1/#sizing
    def parse_anchor_size(self) -> AnchorSizeValue | None:
        # anchor-size() = anchor-size( [ <anchor-name> || <anchor-size> ]? , <length-percentage>? )

        return None

    def parse_angle_value(self) -> AngleValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.DIMENSION and tok.dim_unit in ("deg", "grad", "rad", "turn"):
            self.stream.consume()
            assert isinstance(tok.val, str)
            return AngleValue(float(tok.val), tok.dim_unit)

    def parse_angle_percentage_value(self) -> AngleValue | PercentageValue | None:
        with self.stream.transaction() as tx:
            if angle_value := self.parse_angle_value():
                tx.commit()
                return angle_value
            elif self.stream.peek().type == Tok.PERCENTAGE:
                percentage = self.stream.consume().val
                assert percentage
                tx.commit()
                return PercentageValue(float(percentage))

            # TODO: calc stuff
            # if calc := self.parse_calculated_value() and calc and isinstance(calc, )

    def parse_basic_shape_value(self) -> BasicShapeValue:
        self.stream.consume()
        return BasicShapeValue(BasicShape())

    def parse_color_value(self) -> ColorValue | KeywordValue | None:
        # <color-base> | <system-color> | currentColor
        tok = self.stream.peek()
        if tok.type == Tok.IDENT and tok.val:
            # <color-base>: <named-color>
            if color := Color.from_str(tok.val):
                self.stream.consume()
                return ColorValue(color)

            # <system-color> | currentColor
            keyword = KeywordValue(tok.val)
            if keyword.is_color():
                self.stream.consume()
                return keyword

        # <color-base>: <hex-color>
        elif tok.type == Tok.HASH:
            assert tok.val
            color = Color.from_hash_str(tok.val.val)
            self.stream.consume()
            return ColorValue(color)

    # def parse_corner_shape_value(self) -> CornerShapeValue:
    #     self.stream.consume()
    #     return CornerShapeValue()

    # def parse_counter_value(self) -> CounterValue:
    #     self.stream.consume()
    #     return CounterValue()

    def parse_custom_ident(self, blacklist: list[str]) -> str | None:
        with self.stream.transaction() as tx:
            tok = self.stream.consume()
            if not tok.type == Tok.IDENT:
                return

            if (
                not tok.val
                or tok.val.casefold() == "default"
                or KeywordValue(tok.val).is_css_wide()
            ):
                return

            if tok.val.casefold() in blacklist:
                return

            tx.commit()
            return tok.val

    def parse_custom_ident_value(self, blacklist: list[str]) -> CustomIdentValue | None:
        if custom_ident := self.parse_custom_ident(blacklist):
            return CustomIdentValue(custom_ident)

    def parse_dashed_ident(self) -> str | None:
        with self.stream.transaction() as tx:
            if custom_ident := self.parse_custom_ident(blacklist=[]):
                if not custom_ident.startswith("--"):
                    return
                tx.commit()
                return custom_ident

    def parse_dashed_ident_value(self) -> CustomIdentValue | None:
        if dashed_ident := self.parse_dashed_ident():
            return CustomIdentValue(dashed_ident)

    # def parse_easing_value(self) -> EasingValue:
    #     self.stream.consume()
    #     return EasingValue()

    # def parse_filter_value_list_value(self) -> FilterValueListValue:
    #     self.stream.consume()
    #     return FilterValueListValue()

    # def parse_fit_content_value(self) -> FitContentValue:
    #     self.stream.consume()
    #     return FitContentValue()

    # def parse_flex_value(self) -> FlexValue:
    #     self.stream.consume()
    #     return FlexValue()

    # def parse_frequency_value(self) -> FrequencyValue:
    #     self.stream.consume()
    #     return FrequencyValue()

    # def parse_frequency_percentage_value(self) -> FrequencyPercentageValue:
    #     self.stream.consume()
    #     return FrequencyPercentageValue()

    # def parse_image_value(self) -> ImageValue:
    #     self.stream.consume()
    #     return ImageValue()

    def parse_integer_value(self) -> IntegerValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.NUMBER and tok.num_type == Num.INTEGER and tok.val:
            self.stream.consume()
            return IntegerValue(int(tok.val))

    def parse_length_value(self) -> LengthValue | AnchorSizeValue | None:
        with self.stream.transaction() as tx:
            tok = self.stream.consume()
            if tok.type == Tok.DIMENSION:
                if tok.dim_unit and tok.val and tok.dim_unit in LengthUnit:
                    tx.commit()
                    return LengthValue(Length(float(tok.val), LengthUnit(tok.dim_unit)))

            if tok.type == Tok.NUMBER:
                number = tok.val
                if number == 0:
                    tx.commit()
                    return LengthValue(Length.from_px(0))

        func = self.stream.peek()
        if isinstance(func, Function) and func.name == "anchor-size":
            return self.parse_anchor_size()

        # TODO: parse calc

    def parse_length_percentage_value(
        self,
    ) -> LengthValue | PercentageValue | AnchorSizeValue | None:
        with self.stream.transaction() as tx:
            tok = self.stream.consume()
            if tok.type == Tok.DIMENSION:
                if tok.dim_unit and tok.val and tok.dim_unit in LengthUnit:
                    tx.commit()
                    return LengthValue(Length(float(tok.val), LengthUnit(tok.dim_unit)))

            if tok.type == Tok.PERCENTAGE and tok.val:
                return PercentageValue(float(tok.val))

            if tok.type == Tok.NUMBER:
                number = tok.val
                if number == 0:
                    tx.commit()
                    return LengthValue(Length.from_px(0))

        func = self.stream.peek()
        if isinstance(func, Function) and func.name == "anchor-size":
            return self.parse_anchor_size()

        # TODO: parse calc

    def parse_number_value(self) -> NumberValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.NUMBER and tok.val:
            self.stream.consume()
            return NumberValue(tok.val)

        # TODO: parse calc

    # def parse_opacity_value(self) -> OpacityValue:
    #     self.stream.consume()
    #     return OpacityValue()

    # def parse_opentype_tag_value(self) -> OpentypeTagValue:
    #     self.stream.consume()
    #     return OpentypeTagValue()

    # def parse_paint_value(self) -> PaintValue:
    #     self.stream.consume()
    #     return PaintValue()

    def parse_percentage_value(self) -> PercentageValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.PERCENTAGE and tok.val:
            self.stream.consume()
            return PercentageValue(tok.val)

    # def parse_position_value(
    #     self, type: ValueType = ValueType.POSITION
    # ) -> PositionValue:
    #     self.stream.consume()
    #     return PositionValue()

    # def parse_ratio_value(self) -> RatioValue:
    #     self.stream.consume()
    #     return RatioValue()

    # def parse_rect_value(self) -> RectValue:
    #     self.stream.consume()
    #     return RectValue()

    # def parse_resolution_value(self) -> ResolutionValue:
    #     self.stream.consume()
    #     return ResolutionValue()

    def parse_string_value(self) -> StringValue | None:
        tok = self.stream.peek()
        if tok.type == Tok.STRING and tok.val:
            self.stream.consume()
            return StringValue(tok.val)

    # def parse_time_value(self) -> TimeValue:
    #     self.stream.consume()
    #     return TimeValue()

    # def parse_time_percentage_value(self) -> TimePercentageValue:
    #     self.stream.consume()
    #     return TimePercentageValue()

    # def parse_transform_function_value(self) -> TransformFunctionValue:
    #     self.stream.consume()
    #     return TransformFunctionValue()

    # def parse_transform_list_value(self) -> TransformListValue:
    #     self.stream.consume()
    #     return TransformListValue()

    # def parse_url_value(self) -> URLValue:
    #     self.stream.consume()
    #     return URLValue()
