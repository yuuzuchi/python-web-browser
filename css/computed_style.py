from log import warn
from css.property import keyword_to_keyword_group_keyword
from css.enums import WhiteSpaceCollapse
from css.style_values.color import ColorValue, Color
from css.style_values.display import DisplayValue, Display
from css.style_values.numeric import NumberValue
from css.style_values.dimension import LengthValue
from css.style_values.keyword import KeywordValue
from css.style_values.base import StyleValue
from css.enums import Property, Keyword
from css.color_compute_context import ColorComputeContext
from tkinter.font import Font


class ComputedStyle:
    """Stores computed abstract values (`StyleValue`) for a DOM element
    Provides methods to convert StyleValues into value objects,
    e.g. `computed_line_height()` -> `LengthValue` -> `px: float`
    The `ComputedValue` class, which lives on each `layout` element, stores these value objects.

    *NOTE: Not all of these values can be used directly during the layout/rendering phase.
    The `used/actual` values are produced during the layout phase and stored on each layout node.*
    """

    def __init__(self):
        self.styles: dict[Property, StyleValue] = dict()
        self.font: Font | None = None

    def get(self, property: Property) -> StyleValue | None:
        return self.styles.get(property)

    def computed_color(
        self,
        prop: Property,
        context: ColorComputeContext,
        fallback: Color = Color(0, 0, 0),
    ) -> Color:
        """Requires a property that contains a color (Keyword.is_color)"""
        color = self.styles.get(prop)
        if isinstance(color, ColorValue):
            return color.color
        elif isinstance(color, KeywordValue):
            if color.keyword == Keyword.CURRENTCOLOR:
                return context.current_color
            if color := Color.from_str(color.keyword.value):
                return color
            # TODO: handle system colors
            warn(f"Could not compute color {color}")
        return fallback

    def computed_font_size(self) -> float:
        font_size = self.styles.get(Property.FONT_SIZE)
        assert isinstance(font_size, LengthValue)
        return font_size.length.to_px().value

    def computed_display(self) -> Display:
        if display := self.styles.get(Property.DISPLAY):
            assert isinstance(display, DisplayValue)
            return display.display
        return Display.create_inline()

    def computed_line_height(self) -> float:
        line_height = self.styles.get(Property.LINE_HEIGHT)

        if (
            isinstance(line_height, KeywordValue)
            and line_height.keyword == Keyword.NORMAL
        ):
            return self.computed_font_size() * 1.375

        if isinstance(line_height, LengthValue):
            return line_height.length.to_px().value

        if isinstance(line_height, NumberValue):
            return self.computed_font_size() * line_height.num_value

        assert False, "Line height must be NORMAL, length, or number"
        return self.computed_font_size() * 1.375  # return normal

    def computed_white_space_collapse(self) -> WhiteSpaceCollapse:
        keyword = self.styles.get(Property.WHITE_SPACE_COLLAPSE)
        assert isinstance(keyword, KeywordValue)
        if white_space_collapse := keyword_to_keyword_group_keyword(
            keyword.keyword, WhiteSpaceCollapse
        ):
            assert isinstance(white_space_collapse, WhiteSpaceCollapse)
            return white_space_collapse

        assert False, f"Expected WhiteSpaceCollapse type, but got {keyword}"
        return WhiteSpaceCollapse.COLLAPSE
