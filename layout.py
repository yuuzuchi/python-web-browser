import collections
import random
from draw import DrawRect, DrawText
from font_cache import get_font
from html_parser import Element, Text

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

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)
    
def tree_to_list(tree, l: list):
    l.append(tree)
    for child in tree.children:
        tree_to_list(child, l)
    return l

class DocumentLayout:
    def __init__(self, node, ctx):
        self.node = node
        self.parent = None
        self.children = []
        self.width_cache = collections.defaultdict(dict) # font: {word: width}
        self.ctx = ctx

        self.x = None
        self.y = None
        self.width = None
        self.height = None
    
    def layout(self):
        # clear the tree each time we call layout
        self.children = []
        
        child = BlockLayout([self.node], self, None, self.width_cache) # <html> node
        self.children.append(child)
        self.width = self.ctx.width - 2*MARGINS[0] - MARGINS[4]
        self.x = MARGINS[0]
        self.y = MARGINS[1]
        child.layout()
        self.height = child.height
        
    def paint(self):
        return []

class BlockLayout:
    def __init__(self, nodes: list[Element | Text], parent, previous, width_cache):
        self.nodes = nodes
        self.parent = parent
        self.previous = previous
        self.children = []
        self.width_cache = width_cache

        self.x = None
        self.y = None
        self.width = None
        self.height = None
        
        self._init_state()
    
    def _init_state(self):
        self.align = "left" # center or left
        self.supersub = "normal" # superscript, subscript, or normal
        self.pre = False
        self.current_font = get_font()
        self.display_list = []
        self.line = []
        self.cx, self.cy = 0, 0
        
    def __repr__(self):
        nodes = ""
        children = ""
        for node in self.nodes:
            if isinstance(node, Element):
                nodes += f"{str(node.tag)}, "
            else:
                nodes += f"{str(node.text)}, "

        for child in self.children:
            if isinstance(child, Element):
                children += f"{str(child.tag)}, "
            else:
                children += f"{str(child.text)}, "

        res = f"Nodes: {nodes}, Children: {children}"
        return res

    def paint(self):
        cmds = []
        if len(self.nodes) == 1:
            node = self.nodes[0]
            if isinstance(node, Element):
                bgcolor = node.style.get("background-color", "transparent")
                
                if bgcolor != "transparent":
                    x2, y2 = self.x + self.width, self.y + self.height
                    rect = DrawRect(self.x, self.y, x2, y2, bgcolor)
                    cmds.append(rect)                    
                # # Color pre tags darker
                # if node.tag == "pre":
                #     x2, y2 = self.x + self.width, self.y + self.height
                #     cmds.append(DrawRect(self.x, self.y, x2, y2, "#e9eaf0"))

                # elif node.tag == "nav" and node.attributes.get('class') == 'links':
                #     x2, y2 = self.x + self.width, self.y + self.height
                #     cmds.append(DrawRect(self.x, self.y, x2, y2, "#e9eaf0"))

                # elif node.tag == "nav" and node.attributes.get('id') == 'toc':
                #     cmds.append(DrawRect(self.x, self.y-20, self.x + self.width, self.y, "#e9eaf0"))
                #     ToC_font = get_font(family="Courier New", size=16, style="roman", weight="bold")
                #     cmds.append(DrawText(self.x, self.y-20, "Table of Contents", ToC_font))
                    
                # elif node.tag == "li" and isinstance(node.parent, Element) and node.parent.tag == "ul":
                #     self.current_font
                    
        if self.layout_mode() == "inline":
            for x, y, word, font, color in self.display_list:
                cmds.append(DrawText(x, y, word, font, color))
            
        return cmds
        
    def layout_mode(self) -> bool: 
        """Determine whether to call recurse/flush OR layout_intermediate for each element
           inline = recurse/flush
           block = layout_intermediate"""
        if len(self.nodes) > 1:
            return "inline"

        mode = self.nodes[0].style.get("display")
        if mode in ("block", "none"):
            return mode
        return "inline"
    
    def layout(self):
        mode = self.layout_mode()
        extra_height = 0

        # determine position of our block (width/height auto)
        self.x = self.parent.x
        self.width = self.parent.width
        if len(self.nodes) == 1 and isinstance(self.nodes[0], Element) and \
                self.nodes[0].tag == "nav" and self.nodes[0].attributes.get("id") == "toc":
            extra_height = 20
        self.y = (self.previous.y + self.previous.height if self.previous else self.parent.y) + extra_height

        # this BlockLayout represents a single Text/Element object
        if len(self.nodes) == 1:
            width = self.nodes[0].style.get("width", "auto")
            height = self.nodes[0].style.get("height", "auto")
            if width.endswith("px"):
                self.width = int(width[:-2])
            if height.endswith("px"):
                self.height = int(height[:-2])
                
            if mode == "block":
                self._create_children()
            else:
                self._init_state()
                self.recurse(self.nodes[0])
                self.flush()

        # Represents multiple objects, must be text-like. Recurse over each, then flush
        else:
            self._init_state()
            for node in self.nodes:
                self.recurse(node)
            self.flush()
        
        for child in self.children:
            child.layout()

        self.height = (sum([child.height for child in self.children]) if mode == "block" else self.cy) + extra_height
    
    def _create_children(self):
        node = self.nodes[0] # method is ONLY called when BlockLayout represents single node object
        anonymous_buffer = [] # text-like elements to combine into single BlockLayout
        previous = None
        # print()
        # print(node.tag if isinstance(node, Element) else node.text)
        # print(node.children)
        # print()
        for child in node.children:
            if isinstance(child, Element) and child.tag in BLOCK_ELEMENTS:
                if child.tag in "head":
                    continue

                # flush combinable elements
                if anonymous_buffer:
                    nxt = BlockLayout(anonymous_buffer, self, previous, self.width_cache)
                    anonymous_buffer = []
                    self.children.append(nxt)
                    previous = nxt
                    
                # then add current block element
                # here is where we would handle <li> indenting by appending an InlineLayout with a bullet point
                nxt = BlockLayout([child], self, previous, self.width_cache)
                self.children.append(nxt)
                previous = nxt
            
            # is type text-like, add to anonymous buffer
            else:
                anonymous_buffer.append(child)
            
        # flush remaining buffer at end
        if anonymous_buffer:
            #print(anonymous_buffer)
            self.children.append(BlockLayout(anonymous_buffer, self, previous, self.width_cache))
    
    def open_tag(self, tag):
        tag, attributes = tag.tag, tag.attributes
        if tag == "br":
            self.flush()
            self.cy += self.current_font.cached_metrics['linespace'] * 1.25
        elif tag == 'h1 class="title"':
            self.align = "center"
        elif tag == "sup":
            self.supersub = "superscript"
        elif tag == "sub":
            self.supersub = "subscript"
        
    def close_tag(self, tag):
        tag, attributes = tag.tag, tag.attributes
        if tag == "h1":
            self.flush()
            self.cy += self.current_font.cached_metrics['linespace'] * 1.25
            self.align = "left"
        elif tag in ("sup", "sub"):
            self.supersub = "normal"
        
    def recurse(self, node):
        if isinstance(node, Text):
            family = node.style["font-family"]
            weight = node.style["font-weight"]
            style = node.style["font-style"]
            pre = node.style["white-space"] == "pre"
            if style == "normal": style = "roman"
            size = int(float(node.style["font-size"][:-2]) * .75)
            if self.supersub.startswith("s"): # super/subscript
                size /= 2 

            # within a tag, the font will stay the same
            self.current_font = get_font(family=family, size=size, style=style, weight=weight)
            if pre:
                parts = node.text.split("\n")
                for i, line in enumerate(parts):
                    self.word(node, line, wrap=False)
                    # flush once for each newline in the original text
                    if i < len(parts) - 1:
                        self.flush()
            else:
                for word in node.text.split():
                    self.word(node, word)
        elif node.tag not in NO_RENDER_ELEMENTS:
            self.open_tag(node)
            for child in node.children:
                    self.recurse(child)
            self.close_tag(node)                

    def word(self, node, word, wrap=True):
        color = node.style["color"]
        # get width of word for given style and weight
        word_nohyphen = word.replace("\u00AD", "")
        w = self._get_width(word_nohyphen)
            
        if wrap and self.cx + w > self.width:
            # word cannot be hyphenated, line break now
            if '\u00AD' not in word:
                self.flush()
            else:
                # can be hyphenated, break word as late as possible then recurse on the remaining portion
                parts = word.split('\u00AD')
                idx = self._findsplit(parts) 
                righthalf = '\u00AD'.join(parts[idx+1:])
                
                if idx != -1: 
                    lefthalf = ''.join(parts[:idx+1]) + '-'
                    self.line.append((self.cx, lefthalf, self.current_font, self.supersub, color))
                    
                self.flush()
                self.word(righthalf)
                return
        
        self.line.append((self.cx, word_nohyphen, self.current_font, self.supersub, color))
        self.cx += w
        if not node.style['white-space'] == "pre":
            self.cx += self._get_width(" ")
        
    def flush(self):
        if not self.line: return
        #line_length = self.cx - self.SPACE_WIDTH - MARGINS[0]
        metrics = [font.cached_metrics for _, _, font, _, _ in self.line]
        max_ascent = max(metric["ascent"] for metric in metrics)
        max_descent = max(metric["descent"] for metric in metrics)
        baseline = self.cy + 1.25*max_ascent
        
        # position words so they sit right above the baseline (by their ascent height)
        for rel_x, word, font, supersub, color in self.line:
            x = self.x + rel_x
            # if self.align == "center":
            #     x += (self.ctx.width/2)-(line_length/2)
            if supersub == "superscript":
                # raise superscript text by moving it up by half the font's ascent
                y = self.y + baseline - (2 * font.cached_metrics["ascent"])
            else:
                y = self.y + baseline - font.cached_metrics["ascent"]
            self.display_list.append((x, y, word, font, color))

        # move cursor below deepest descent
        self.cy = baseline + 1.25*max_descent

        # reset to left
        self.cx = 0
        self.line = []

    def _get_width(self, word):
        font_id = self.current_font.id
        if word in self.width_cache[font_id]:
            return self.width_cache[font_id][word]
        else:
            w = self.current_font.measure(word)
            self.width_cache[font_id][word] = w
            return w

    def _findsplit(self, parts):
        # binary search for latest possible place to hyphenate word
        l, r = 0, len(parts)-1
        ans = -1
        while l <= r:
            mid = (l + r) // 2
            leftword = ''.join(parts[:mid+1]) + "-"
            w = self.current_font.measure(leftword)

            if self.cx + w <= self.width:
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return ans