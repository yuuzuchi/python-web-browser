from dom import Element
from layout.box import Box


class BreakBox(Box):
    def __init__(self, node: Element, parent):
        super().__init__(node, parent, None)

    def __repr__(self):
        tag = getattr(self.node, "tag", "br")
        return f"<BreakLayout {tag} x={self.x} y={self.y}>"
