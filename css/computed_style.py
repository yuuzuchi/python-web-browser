from dataclasses import field
from css.style_values.base import StyleValue
from css.enums import Property
from dataclasses import dataclass
from tkinter.font import Font


@dataclass
class ComputedStyle:
    styles: dict[Property, StyleValue] = field(init=False, default_factory=dict)
    font: Font | None = field(init=False, default=None)

    def get(self, property: Property) -> StyleValue | None:
        return self.styles.get(property)
