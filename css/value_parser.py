from css.style_values import Color
from css.style_values import *
from css.token_stream import CSSTokenStream
from enums import Property, ValueType


class ValueParser:
    def __init__(self, inp: list | CSSTokenStream):
        self.stream = inp
        if not isinstance(inp, CSSTokenStream):
            self.stream = CSSTokenStream(inp)

    def set_context(self, property: Property):
        self.property = property

    def parse(self, type: ValueType) -> StyleValue:
        match type:
            case ValueType.ANCHOR:
                return self.parse_anchor_value()
            case ValueType.ANCHOR_SIZE:
                return self.parse_anchor_size_value()
            case ValueType.ANGLE:
                return self.parse_angle_value()
            case ValueType.ANGLE_PERCENTAGE:
                return self.parse_angle_percentage_value()
            case ValueType.BACKGROUND_POSITION:
                return self.parse_position_value(ValueType.BACKGROUND_POSITION)
            case ValueType.BASIC_SHAPE:
                return self.parse_basic_shape_value()
            case ValueType.COLOR:
                return self.parse_color_value()
            case ValueType.CORNER_SHAPE:
                return self.parse_corner_shape_value()
            case ValueType.COUNTER:
                return self.parse_counter_value()
            case ValueType.CUSTOM_IDENT:
                return self.parse_custom_ident_value()
            case ValueType.DASHED_IDENT:
                return self.parse_dashed_ident_value()
            case ValueType.EASING_FUNCTION:
                return self.parse_easing_value()
            case ValueType.FILTER_VALUE_LIST:
                return self.parse_filter_value_list_value()
            case ValueType.FIT_CONTENT:
                return self.parse_fit_content_value()
            case ValueType.FLEX:
                return self.parse_flex_value()
            case ValueType.FREQUENCY:
                return self.parse_frequency_value()
            case ValueType.FREQUENCY_PERCENTAGE:
                return self.parse_frequency_percentage_value()
            case ValueType.IMAGE:
                return self.parse_image_value()
            case ValueType.INTEGER:
                return self.parse_integer_value()
            case ValueType.LENGTH:
                return self.parse_length_value()
            case ValueType.LENGTH_PERCENTAGE:
                return self.parse_length_percentage_value()
            case ValueType.NUMBER:
                return self.parse_number_value()
            case ValueType.OPACITY:
                return self.parse_opacity_value()
            case ValueType.OPENTYPE_TAG:
                return self.parse_opentype_tag_value()
            case ValueType.PAINT:
                return self.parse_paint_value()
            case ValueType.PERCENTAGE:
                return self.parse_percentage_value()
            case ValueType.POSITION:
                return self.parse_position_value()
            case ValueType.RATIO:
                return self.parse_ratio_value()
            case ValueType.RECT:
                return self.parse_rect_value()
            case ValueType.RESOLUTION:
                return self.parse_resolution_value()
            case ValueType.STRING:
                return self.parse_string_value()
            case ValueType.TIME:
                return self.parse_time_value()
            case ValueType.TIME_PERCENTAGE:
                return self.parse_time_percentage_value()
            case ValueType.TRANSFORM_FUNCTION:
                return self.parse_transform_function_value()
            case ValueType.TRANSFORM_LIST:
                return self.parse_transform_list_value()
            case ValueType.URL:
                return self.parse_url_value()
            case _:
                assert False, "nonexistant value type"

    def parse_angle_value(self) -> AngleValue:
        tok = self.stream.peek()
        if tok.type == Tok.DIMENSION and tok.dim_unit in ("deg", "grad", "rad", "turn"):
            self.stream.consume()
            return AngleValue(tok.val, tok.dim_unit)

    def parse_color_value(self) -> ColorValue | KeywordValue:
        # <color-base> | <system-color> | currentColor
        tok = self.stream.peek()
        if tok.type == Tok.IDENT:
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
            color = Color.from_hash_str(tok.val.val)
            self.stream.consume()
            return ColorValue(color)

    def parse_integer_value(self) -> IntegerValue:
        tok = self.stream.peek()
        if tok.type == Tok.NUMBER and tok.num_type == Num.INTEGER:
            self.stream.consume()
            return NumberValue(int(tok.val))

    def parse_number_value(self) -> NumberValue:
        tok = self.stream.peek()
        if tok.type == Tok.NUMBER:
            self.stream.consume()
            return NumberValue(tok.val)

    def parse_percentage_value(self) -> PercentageValue:
        tok = self.stream.peek()
        if tok.type == Tok.PERCENTAGE:
            self.stream.consume()
            return PercentageValue(tok.val)

    def parse_string_value(self) -> StringValue:
        tok = self.stream.peek()
        if tok.type == Tok.STRING:
            self.stream.consume()
            return StringValue(tok.val)
