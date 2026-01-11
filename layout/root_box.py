from layout.layout import MARGINS
from layout.box import Box
import tkinter


class RootBox(Box):
    def __init__(self, node, canvas: tkinter.Canvas):
        super().__init__(node, None, None)
        self.canvas = canvas

    def layout(self):
        assert self.node, "root box must have an associated HTMl element"
        from layout.tree_builder import build_layout_for_node

        child = build_layout_for_node(self.node, self, None)  # <html> node
        self.children = [child]
        self.width = self.canvas.winfo_width() - 2 * MARGINS[0] - MARGINS[4]
        self.x = MARGINS[0]
        self.y = MARGINS[1]

        from layout.formatting_context import BlockFormattingContext

        BlockFormattingContext(child).format()
        self.height = child.height

    def paint(self):
        return []
