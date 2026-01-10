from css.computed_style import ComputedStyle
from url import URL
from css.enums import Property
from css.style_values.base import StyleValue


class Node:
    def __init__(self, parent):
        self.parent: Element = parent
        self.children: list["Node"] = []
        self.computed_style: ComputedStyle = ComputedStyle()
        self.specified_style: dict[Property, StyleValue] = {}

    def get_root(self) -> "Node":
        """Walks the tree up towards the root HTML element and returns it"""
        cur = self
        while cur.parent:
            cur = cur.parent
        return cur


class Text(Node):
    def __init__(self, text, parent):
        """A text node, found only within a parent Element node. Must be a leaf node."""
        super().__init__(parent)
        self.text = text
        self.classes = set()

    def __repr__(self):
        return f"{self.text}, style={self.computed_style}"


class Element(Node):
    def __init__(
        self,
        tag: str,
        attributes: dict[str, str],
        parent: Node | None,
        classes: set[str],
    ):
        """A node in a document, corresponds to an HTML tagged element.
        tags and attribute names are case insensitive (but attribute values are sensitive!)
        """
        super().__init__(parent)
        self.tag = tag.casefold()
        self.attributes = attributes
        self.classes = classes

    def __repr__(self):
        return f"<{self.tag}>{str(self.attributes) if self.attributes else ""}, style={self.computed_style}, class={self.classes}"


class Document:
    def __init__(self, document_element: Element, url: URL):
        self.document_element = document_element
        document_element.owner_document = self
        self.url = url
