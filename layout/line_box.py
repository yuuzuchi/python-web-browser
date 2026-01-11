from layout.text_fragment import TextFragment
from dom import Node


class LineBox:
    """NOT produced by element and do NOT have their own styles!
    Product of InlineFormattingContext"""
    def __init__(self, node: Node):
        self.node = node
        self.x = self.y = self.width = self.height = 0
        self.children: list[TextFragment] = []

    def __repr__(self):
        return f"<LineBox x={self.x} y={self.y} children={len(self.children)}>"
