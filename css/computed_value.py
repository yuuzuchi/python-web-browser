from typing import Optional
from css.enums import WhiteSpaceCollapse
from css.style_values.color import Color
from css.style_values.display import Display
from tkinter.font import Font


class ComputedValue:
    def __init__(self, font: Font):
        self.font = font

        self.color = Color(0, 0, 0)
        self.background_color = self.color

        self.font_size = 16
        self.display = Display.create_inline()
        self.line_height = self.font_size * 1.375
        self.white_space_collapse = WhiteSpaceCollapse.COLLAPSE

    def __repr__(self):
        return (
            f"ComputedValue(font={self.font}, color={self.color}, "
            f"font_size={self.font_size}, display={repr(self.display)}, "
            f"line_height={self.line_height}, white_space_collapse={self.white_space_collapse})"
        )
