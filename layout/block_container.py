from layout.inline_box import InlineBox
from draw import DrawRect
from css.style_values.color import Color
from dom import Element
from font_cache import get_font
from layout.box import Box
from dom import Node


class BlockContainer(Box):
    # corresponds to `BlockLayout` in the textbook

    def __init__(
        self,
        node: Node | None,
        parent: Box,
        previous: Box | None,
    ):
        super().__init__(node, parent, previous)
        self.align = "left"  # center or left
        self.supersub = "normal"  # superscript, subscript, or normal
        self.pre = False
        self.current_font = get_font()
        self.cx = 0

    def __repr__(self):
        tag = getattr(self.node, "tag", None)
        kind = tag if tag is not None else "anonymous"
        return f"<BlockContainer {kind} x={self.x} y={self.y} w={self.width} h={self.height} children={len(self.children)}>"

    def paint(self):
        cmds = []
        if isinstance(self.node, Element):
            bgcolor = self.computed_style().background_color
            if bgcolor != Color(0, 0, 0, 0):
                rect = DrawRect(self.self_rect(), bgcolor.to_hex_str()[:7])
                cmds.append(rect)

        return cmds

    def has_inline_children(self):
        if self.is_anonymous():
            return True

        for child in self.children:
            if isinstance(child, InlineBox):
                return True
        return False
