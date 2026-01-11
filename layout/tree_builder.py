from typing import Iterator
from layout.root_box import RootBox
from layout.break_box import BreakBox
from layout.box import Box
from layout.inline_box import InlineBox
from dom import Element
from layout.block_container import BlockContainer
from layout.text_box import TextBox
from dom import Node
from dom import Text


def build_layout_for_node(node: Node, parent, previous):
    style = node.computed_style
    if style.computed_display().is_block():
        box = BlockContainer(node, parent, previous)

        inline_buffer = []
        prev_child = None
        for child in node.children:
            if (
                isinstance(child, Element)
                and child.computed_style.computed_display().is_block()
            ):
                if child.tag == "head":
                    continue

                # flush combinable (inline) elements
                if inline_buffer:
                    anon = BlockContainer(None, box, prev_child)
                    anon.children = build_inline_layouts(inline_buffer, anon)
                    if anon.children:
                        box.children.append(anon)
                        prev_child = anon
                    inline_buffer = []

                # then add our current block element
                child_box = build_layout_for_node(child, box, prev_child)
                if child_box:
                    box.children.append(child_box)
                    prev_child = child_box

            # inline type, extend buffer
            else:
                inline_buffer.append(child)

        # flush trailing elements in buffer
        if inline_buffer:
            anon = BlockContainer(None, box, prev_child)
            anon.children = build_inline_layouts(inline_buffer, anon)
            if anon.children:
                box.children.append(anon)
        return box

    else:
        # top level (usually <html>) contains pure inline text
        box = InlineBox(node, parent)
        box.children = build_inline_layouts([node], box)
        return box


def build_inline_layouts(nodes: list[Node], parent) -> list[Box]:
    # print("build inline for nodes", nodes)
    res = []
    for node in nodes:
        if isinstance(node, Element):
            if node.tag == "head":
                continue
            elif node.computed_style.computed_display().is_none():
                continue
            elif node.tag == "br":
                br = BreakBox(node, parent)
                res.append(br)
            elif node.computed_style.computed_display().is_inline():
                elem = InlineBox(node, parent)
                elem.children = build_inline_layouts(node.children, elem)
                res.append(elem)
        elif isinstance(node, Text):
            textbox = TextBox(node, node.text, parent)
            res.append(textbox)
    return res


# given the children of a Block type Layout (BlockLayout or AnonymousLayout) that contains inline children,
# walk children in preorder dfs traversal
def flatten(layouts: list[Box]) -> Iterator[TextBox | BreakBox]:
    for layout in layouts:
        # base case; no children
        if isinstance(layout, TextBox) or isinstance(layout, BreakBox):
            yield layout
            continue

        # yield children
        if isinstance(layout, InlineBox):
            for child in layout.children:
                yield from flatten([child])

        else:  # children somehow contain block layout
            raise AssertionError


def paint_tree(layout_object: Box, display_list):
    display_list.extend(layout_object.paint())

    if layout_object.line_boxes != []:
        paint_inline(layout_object.line_boxes, display_list)
        return

    for child in layout_object.children:
        if isinstance(child, (RootBox, BlockContainer)):
            paint_tree(child, display_list)


def print_layout_tree(layout_object: Box):
    def _print(node: Box, depth: int):
        indent = ".." * depth
        try:
            line = repr(node)
        except Exception:
            line = f"<{node.__class__.__name__}>"
        print(indent + line)
        for child in getattr(node, "children", []):
            _print(child, depth + 1)

    _print(layout_object, 0)


# only text fragments can be painted
def paint_inline(line_boxes, display_list):
    for line in line_boxes:
        for text_frag in line.children:
            paint = text_frag.paint()
            if paint:
                display_list.extend(paint)


def print_paint(display_list):
    for cmd in display_list:
        print(cmd)


def tree_to_list(tree):
    yield tree
    for child in tree.children:
        yield from tree_to_list(child)


def tree_to_fragment_list(tree: Box):
    if tree.line_boxes != []:
        for line in tree.line_boxes:
            yield from line.children

    if isinstance(tree, (RootBox, BlockContainer)):
        for child in tree.children:
            yield from tree_to_fragment_list(child)
