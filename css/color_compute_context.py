from __future__ import annotations
from typing import TYPE_CHECKING
from css.enums import Property
from css.style_values.color import Color
from dataclasses import dataclass

if TYPE_CHECKING:
    from dom import Node


@dataclass
class ColorComputeContext:
    current_color: Color

    @classmethod
    def from_element(cls, node: Node) -> ColorComputeContext:
        """Creates a ColorComputeContext using given DOM element's `COLOR` property.
        Fallback to black otherwise."""
        computed_color = node.computed_style.computed_color(
            Property.COLOR, ColorComputeContext(current_color=Color(0, 0, 0))
        )

        return ColorComputeContext(current_color=computed_color)
