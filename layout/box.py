from __future__ import annotations
from draw import Rect
from css.enums import Property
from css.color_compute_context import ColorComputeContext
from font_cache import get_font
from css.computed_value import ComputedValue
from dom import Node


class Box:
    def __init__(
        self,
        node: Node | None,
        parent: Box | None,
        previous: Box | None,
    ):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.x = self.y = self.width = self.height = 0
        self.line_boxes = []  # computed lines to paint from self.children
        self._computed_style = ComputedValue(get_font())
        self.apply_computed_styles()

    def apply_computed_styles(self):
        if not self.node:
            # for anonymous boxes, copy style from parent
            if self.parent:
                self._computed_style = self.parent._computed_style
                return

            assert False, type(self)

        computed_style = self.node.computed_style
        style = self._computed_style
        if computed_style.font:
            style.font = computed_style.font
        color_compute_context = ColorComputeContext.from_element(self.node)
        style.color = computed_style.computed_color(
            Property.COLOR, color_compute_context
        )
        style.background_color = computed_style.computed_color(
            Property.BACKGROUND_COLOR, color_compute_context
        )
        style.display = computed_style.computed_display()
        style.line_height = computed_style.computed_line_height()
        style.white_space_collapse = computed_style.computed_white_space_collapse()

    def self_rect(self):
        return Rect(self.x, self.y, self.x + self.width, self.y + self.height)

    def computed_style(self) -> ComputedValue:
        return self._computed_style

    def has_inline_children(self) -> bool:
        return False

    def is_anonymous(self) -> bool:
        return not self.node

    def paint(self):
        return []
