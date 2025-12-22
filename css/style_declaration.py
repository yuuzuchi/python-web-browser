from dataclasses import dataclass
from css.property import Property
from css.style_values.base import StyleValue


@dataclass
class StyleDeclaration:
    prop: Property
    val: StyleValue
    important: bool = False

    def __str__(self):
        return f"{self.prop}: {self.val}{" !important" if self.important else ""};"