from draw import DrawText
import tkinter
from layout.box import Box


class TextFragment:

    def __init__(
        self,
        parent_layout: Box,
        text: str,
        x: int,
        y: int,
        width: int,
        font: tkinter.font.Font,
        color: str,
    ):
        self.parent_layout = parent_layout
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.color = color

    def paint(self):
        if self.text:
            return [
                DrawText(self.x, self.y, self.text, self.width, self.font, self.color)
            ]
