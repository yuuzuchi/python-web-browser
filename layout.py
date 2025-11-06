import collections
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

MARGINS = [10, 10, 20, 10] # left, top, right, bottom

def paint_tree(layout_object, display_list):
  display_list.extend(layout_object.paint())

  for child in layout_object.children:
    paint_tree(child, display_list)

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
        child = BlockLayout(self.node, self, None, self.width_cache) # <html> node
        self.children.append(child)
        self.width = self.ctx.width - 2*MARGINS[0]
        self.x = MARGINS[0]
        self.y = MARGINS[1]
        child.layout()
        self.height = child.height
        
    def paint(self):
        return []

class BlockLayout:
    def __init__(self, node, parent, previous, width_cache):
        self.node = node
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
        self.style = "roman"
        self.weight = "normal"
        self.size = 12
        self.align = "left" # center or left
        self.supersub = "normal" # superscript, subscript, or normal
        self.pre = False
        self.SPACE_WIDTH = get_font(size=self.size, style=self.style, weight=self.weight).measure(" ")
        self.LINESPACE = get_font(size=self.size, style=self.style, weight=self.weight).metrics("linespace")*1.25
        self.current_font = get_font()
        self.display_list = []
        self.line = []
        self.cx, self.cy = 0, 0

    def paint(self):
        cmds = []
        # Color pre tags darker
        if isinstance(self.node, Element) and self.node.tag == "pre":
            x2, y2 = self.x + self.width, self.y + self.height
            cmds.append(DrawRect(self.x, self.y, x2, y2, "#e9eaf0"))
            
        if self.layout_mode() == "inline":
            for x, y, word, font in self.display_list:
                cmds.append(DrawText(x, y, word, font))
        self.display_list = [] # clear output for next paint call
            
        return cmds
        
    def layout_mode(self) -> bool: 
        """Determine whether to call recurse/flush OR layout_intermediate for each element
           inline = recurse/flush
           block = layout_intermediate"""
        if isinstance(self.node, Text):
            return "inline"
        # if any children that are block element tags:
        # prevents children like <b> from creating a new block
        # if block and inline children both exist, default to block
        elif any([isinstance(child, Element) and child.tag in BLOCK_ELEMENTS for child in self.node.children]):
            return "block"
        elif self.node.children:
            return "inline"
        return "block" # self closing tags
    
    def layout(self):
        # determine position of our block
        self.x = self.parent.x
        self.width = self.parent.width
        self.y = self.previous.y + self.previous.height if self.previous else self.parent.y
        
        mode = self.layout_mode()
        if mode == "block":
            previous = None
            for child in self.node.children:
                nxt = BlockLayout(child, self, previous, self.width_cache)
                self.children.append(nxt)
                previous = nxt
        else:
            self._init_state()
            self.recurse(self.node)
            self.flush()
        
        for child in self.children:
            child.layout()

        self.height = sum([child.height for child in self.children]) if mode == "block" else self.cy
    
    def open_tag(self, tag):
        if tag in ("i", "em"):
            self.style = "italic"
        elif tag in ("b", "strong"):
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()
            self.cy += self.current_font.cached_metrics['linespace'] * 1.25
        elif tag == 'h1 class="title"':
            self.align = "center"
        elif tag == "sup":
            self.supersub = "superscript"
        elif tag == "sub":
            self.supersub = "subscript"
        elif tag == "pre":
            self.pre = True
            self.flush()
        
    def close_tag(self, tag):
        if tag in ("i", "em"):
            self.style = "roman"
        elif tag in ("b", "strong"):
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "p":
            self.flush()
            self.cy += self.current_font.cached_metrics['linespace'] * 1.25
        elif tag == "h1":
            self.flush()
            self.cy += self.current_font.cached_metrics['linespace'] * 1.25
            self.align = "left"
        elif tag in ("sup", "sub"):
            self.supersub = "normal"
        elif tag == "pre":
            self.pre = False
            self.flush()
        
    def recurse(self, tree):
        if isinstance(tree, Text):
            # halve font size if super/subscript
            size = self.size/2 if self.supersub.startswith("s") else self.size

            if self.pre:
                # pre block, print line by line and dont wrap
                # within a tag, the font will stay the same
                self.current_font = get_font(family="Courier New", size=size, style=self.style, weight=self.weight)
                if "\n" in tree.text:
                    first = True
                    for line in tree.text.split("\n"):
                        if not first:
                            self.flush()
                        first = False
                        self.word(line, wrap=False)
                else:
                    # no newlines in pre block, send entire text
                    self.word(tree.text, wrap=False)
            else:
                # no pre block, process word by word
                self.current_font = get_font(size=size, style=self.style, weight=self.weight)
                for word in tree.text.split():
                    self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)                

    def word(self, word, wrap=True):
        # get width of word for given style and weight
        font_id = self.current_font.id
        
        word_nohyphen = word.replace("\u00AD", "")
        
        if word_nohyphen in self.width_cache[font_id]:
            w = self.width_cache[font_id][word_nohyphen]
        else:
            w = self.current_font.measure(word_nohyphen)
            self.width_cache[font_id][word_nohyphen] = w
            
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
                    self.line.append((self.cx, lefthalf, self.current_font, self.supersub))
                    
                self.flush()
                self.word(righthalf)
                return
        
        self.line.append((self.cx, word_nohyphen, self.current_font, self.supersub))
        self.cx += w + self.SPACE_WIDTH
        
    def flush(self):
        if not self.line: return
        #line_length = self.cx - self.SPACE_WIDTH - MARGINS[0]
        metrics = [font.cached_metrics for _, _, font, _ in self.line]
        max_ascent = max(metric["ascent"] for metric in metrics)
        max_descent = max(metric["descent"] for metric in metrics)
        baseline = self.cy + 1.25*max_ascent
        
        # position words so they sit right above the baseline (by their ascent height)
        for rel_x, word, font, supersub in self.line:
            x = self.x + rel_x
            # if self.align == "center":
            #     x += (self.ctx.width/2)-(line_length/2)
            if supersub == "superscript":
                # raise superscript text by moving it up by half the font's ascent
                y = self.y + baseline - (2 * font.cached_metrics["ascent"])
            else:
                y = self.y + baseline - font.cached_metrics["ascent"]
            self.display_list.append((x, y, word, font))

        # move cursor below deepest descent
        self.cy = baseline + 1.25*max_descent

        # reset to left
        self.cx = 0
        self.line = []

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