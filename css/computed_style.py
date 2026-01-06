from css.style_values.dimension import Length
from css.style_values.numeric import NumberValue
from css.style_values.dimension import LengthValue
from dataclasses import field, dataclass
from css.style_values.keyword import KeywordValue
from css.style_values.base import StyleValue
from css.enums import Property, Keyword
from tkinter.font import Font


@dataclass
class ComputedStyle:
    styles: dict[Property, StyleValue] = field(init=False, default_factory=dict)
    font: Font | None = field(init=False, default=None)

    def get(self, property: Property) -> StyleValue | None:
        return self.styles.get(property)

    def computed_font_size(self) -> float:
        font_size = self.styles.get(Property.FONT_SIZE)
        assert isinstance(font_size, LengthValue)
        return font_size.length.to_px().value

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
