from dataclasses import dataclass
import tkinter
from typing import Iterator, Optional
from draw import DrawRect, DrawText, Rect
from font_cache import get_font
from html_parser import Element, Text
from url import URL

BLOCK_ELEMENTS = [
    "html", "body", "article", "section", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
    "footer", "address", "p", "hr", "pre", "blockquote",
    "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
    "figcaption", "main", "div", "table", "form", "fieldset",
    "legend", "details", "summary"
]

NO_RENDER_ELEMENTS = [
    "script", "style", "title", "meta", "link", "base", "template"
]

MARGINS = [10, 10, 20, 10, 16] # left, top, right, bottom, scrollbar padding

class Layout:
    def __init__(self, node: Element | Text | None, parent: Optional["Layout"], previous: Optional["Layout"]):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.x = self.y = self.width = self.height = None
        self.line_boxes = [] # computed lines to paint from self.children

    def self_rect(self):
        return Rect(self.x, self.y, self.x+self.width, self.y+self.height)

    def computed_style(self):
        return self.node.style if self.node else None

class DocumentLayout(Layout):

    def __init__(self, node, canvas: tkinter.Canvas):
        super().__init__(node, None, None)
        self.canvas = canvas

    def layout(self):
        child = build_layout_for_node(self.node, self, None) # <html> node
        self.children = [child]
        self.width = self.canvas.winfo_width() - 2*MARGINS[0] - MARGINS[4]
        self.x = MARGINS[0]
        self.y = MARGINS[1]
        
        from formatting_context import BlockFormattingContext
        BlockFormattingContext(child).format()
        self.height = child.height

    def paint(self):
        return []

class BlockLayout(Layout):
    def __init__(self, node: Element|Text, parent: Element|Text|None, previous: Element|Text|None):
        super().__init__(node, parent, previous)
        self.align = "left" # center or left
        self.supersub = "normal" # superscript, subscript, or normal
        self.pre = False
        self.current_font = get_font()
        self.cx = 0

    def __repr__(self):
        tag = getattr(self.node, "tag", None)
        kind = tag if tag is not None else "text-block"
        return f"<BlockLayout {kind} x={self.x} y={self.y} w={self.width} h={self.height} children={len(self.children)}>"

    def paint(self):
        cmds = []
        if isinstance(self.node, Element):
            bgcolor = self.node.style.get("background-color", "transparent")
            if bgcolor != "transparent":
                rect = DrawRect(self.self_rect(), bgcolor)
                cmds.append(rect)                    

        return cmds

    def has_inline_children(self):
        for child in self.children:
            if isinstance(child, InlineElementLayout):
                return True
        return False

class AnonymousLayout(Layout):
    def __init__(self, parent, previous):
        super().__init__(None, parent, previous)

    def computed_style(self):
        return self.parent.node.style

    def paint(self):
        return []

    def has_inline_children(self):
        return self.children != [] # should in theory always be True

    def __repr__(self):
        parent_tag = None
        if getattr(self.parent, "node", None) is not None:
            parent_tag = getattr(self.parent.node, "tag", None) or "anon-parent"
        return f"<AnonymousLayout parent={parent_tag} x={self.x} y={self.y} w={self.width} h={self.height} children={len(self.children)}>"

class LineLayout(Layout):
    def __init__(self, node):
        super().__init__(node, None, None)

    def __repr__(self):
        return f"<LineLayout x={self.x} y={self.y} children={len(self.children)}>"

class TextLayout(Layout):
    def __init__(self, node, text_run, parent):
        super().__init__(node, parent, None)
        self.text_run = text_run

    def __repr__(self):
        txt = (self.text_run[:16] + "...") if self.text_run and len(self.text_run) > 16 else (self.text_run or "")
        return f"<TextLayout '{txt}' x={self.x} y={self.y} w={self.width} h={self.height}>"

class TextFragment:
    def __init__(self, parent_layout: Layout, text: str, x: int, y: int, width: int, font: tkinter.font.Font, color: str):
        self.parent_layout = parent_layout
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.color = color
        
    def paint(self):
        if self.text:
            return [DrawText(self.x, self.y, self.text, self.width, self.font, self.color)]

class BreakLayout(Layout):
    def __init__(self, node: Element, parent):
        super().__init__(node, parent, None)
        
    def __repr__(self):
        tag = getattr(self.node, "tag", "br")
        return f"<BreakLayout {tag} x={self.x} y={self.y}>"

class InlineElementLayout(Layout):
    def __init__(self, node, parent):
        super().__init__(node, parent, None)
    
    def __repr__(self):
        tag = getattr(self.node, "tag", None)
        return f"<InlineElementLayout {tag} children={len(self.children)}>"

def build_layout_for_node(node: Element|Text, parent, previous):
    style = node.style
    if style["display"] == "block":
        box = BlockLayout(node, parent, previous)
        
        inline_buffer = []
        prev_child = None
        for child in node.children:
            if isinstance(child, Element) and child.style.get("display") == "block":
                if child.tag == "head":
                    continue
                
                # flush combinable (inline) elements
                if inline_buffer:
                    anon = AnonymousLayout(box, prev_child)
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
            anon = AnonymousLayout(box, prev_child)
            anon.children = build_inline_layouts(inline_buffer, anon)
            if anon.children:
                box.children.append(anon)
        return box
    
    else:
        # top level (usually <html>) contains pure inline text
        box = InlineElementLayout(node, parent)
        box.children = build_inline_layouts([node], box)
        return box

def build_inline_layouts(nodes: list[Element|Text], parent) -> list[Layout]:
    res = []
    for node in nodes:
        if isinstance(node, Element):
            if node.tag == "head":
                continue
            if node.tag in NO_RENDER_ELEMENTS or node.style.get("display") == "none": continue
            if node.tag == "br": 
                br = BreakLayout(node, parent)
                res.append(br)
            elif node.style.get("display") == "inline" or node.tag not in BLOCK_ELEMENTS:
                elem = InlineElementLayout(node, parent)
                elem.children = build_inline_layouts(node.children, parent)
                res.append(elem)
        else:
            textbox = TextLayout(node, node.text, parent)
            res.append(textbox)
    return res

# given the children of a Block type Layout (BlockLayout or AnonymousLayout) that contains inline children,
# walk children in preorder dfs traversal
def flatten(layouts: list[Layout]) -> Iterator[TextLayout | BreakLayout]:
    for layout in layouts:
        # base case; no children
        if isinstance(layout, TextLayout) or isinstance(layout, BreakLayout):
            yield layout
            continue
        
        # yield children
        if isinstance(layout, InlineElementLayout):
            for child in layout.children:
                yield from flatten([child])
        
        else: # children somehow contain block layout
            assert False

def paint_tree(layout_object: Layout, display_list):
    display_list.extend(layout_object.paint())
    
    if layout_object.line_boxes != []:
        paint_inline(layout_object.line_boxes, display_list)
        return 
    
    for child in layout_object.children:
        if isinstance(child, (DocumentLayout, BlockLayout, AnonymousLayout)):
            paint_tree(child, display_list)

def print_layout_tree(layout_object: Layout):
    def _print(node: Layout, depth: int):
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

def tree_to_fragment_list(tree: Layout):
    if tree.line_boxes != []:
        for line in tree.line_boxes:
            yield from line.children
            
    if isinstance(tree, (DocumentLayout, BlockLayout, AnonymousLayout)):
        for child in tree.children:
            yield from tree_to_fragment_list(child)
