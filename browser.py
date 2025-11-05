import collections
import tkinter
from font_cache import get_font
from html_parser import HTMLParser, Text, Element, print_tree
from url import URL
from dataclasses import dataclass

WIDTH, HEIGHT = 1280, 720
MARGINS = [10, 10, 20, 10] # left, top, right, bottom
SCROLL_STEP = 60

@dataclass
class scrollstate:
    is_dragging: bool = False
    drag_offset: int = 0
    pos: int = 0
    bar_y: int = 0
    bar_height: int = 0

class Browser:
    def __init__(self, options: dict={}):
        """Options:
        - rtl: bool, Right to Left text direction rendering"""
        self.width, self.height = WIDTH, HEIGHT
        self.window = tkinter.Tk()
        self.window.configure(bg="white")
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg="white"
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Button-4>", self.scrollup)
        self.window.bind("<Button-5>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.scrolldelta)
        self.window.bind("<Button-1>", self.on_mouse_down)
        self.window.bind("<B1-Motion>", self.on_mouse_drag)
        self.window.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        self.scroll = scrollstate()
        self.nodes = []
        self.text_height = 0
        self.rtl = options.get("rtl", False)
        
        self.layout = Layout()
        self.display_list = []
        
    def resize_canvas(self, e):
        self.width = e.width
        self.height = e.height
        self.canvas.config(width=self.width, height=self.height)
        self._layout()
    
    def draw(self):
        self.canvas.delete("all")
        self.draw_scrollbar()
        for x, y, t, font in self.display_list:
            if y > self.scroll.pos + self.height: continue
            if y + MARGINS[3] < self.scroll.pos: continue
            self.canvas.create_text(x, y - self.scroll.pos, text=t, anchor='nw', font=font)
            
    def draw_scrollbar(self):
        if self.height >= self.text_height:
            return
        self.canvas.create_rectangle(self.width-10, 0, self.width, self.height, width=0, fill="#cccccc")
        self.scroll.bar_height = self.height**2 / self.text_height
        self.scroll.bar_y = self.scroll.pos*self.height / self.text_height
        self.canvas.create_rectangle(self.width-10, self.scroll.bar_y, self.width, self.scroll.bar_y+self.scroll.bar_height, width=0, fill="#aaaaaa")
    
    def load(self, url: URL):
        body = url.request()
        self.nodes = HTMLParser(body).parse()
        print_tree(self.nodes)
        print("\nCalculating layout...\n")
        self._layout()
    
    def _layout(self):
        self.display_list = self.layout.calculate(self.nodes, self.width)
        self.text_height = self.display_list[-1][1] + 20 if self.display_list else 0# height of last object to draw
        self.constrain_scroll()
        self.draw()
        
    def scrolldown(self, e):
        """Down arrow / Linux mouse wheel down"""
        self.scroll.pos += SCROLL_STEP
        self.constrain_scroll()
        self.draw()
    
    def scrollup(self, e):
        """Up arrow / Linux mouse wheel up"""
        self.scroll.pos -= SCROLL_STEP
        self.constrain_scroll()
        self.draw()
        
    def scrolldelta(self, e):
        """Windows / macOS scroll"""
        self.scroll.pos = self.scroll.pos + e.delta
        self.constrain_sroll()
        self.draw()
        
    def constrain_scroll(self):
        self.scroll.pos = min(self.scroll.pos, self.text_height-self.height+MARGINS[3])
        self.scroll.pos = max(0, self.scroll.pos)

    def on_mouse_down(self, e):
        # handle scrollbar drag
        if e.y >= self.scroll.bar_y and e.y <= self.scroll.bar_y + self.scroll.bar_height and \
                e.x >= self.width-10 and e.x < self.width:
            self.scroll.is_dragging = True
            self.scroll.drag_offset = e.y - self.scroll.bar_y
    
    def on_mouse_drag(self, e):
        # scrollbar drag
        if self.scroll.is_dragging:
            bar_y = e.y - self.scroll.drag_offset
            self.scroll.pos = self.text_height * bar_y / self.height
            self.constrain_scroll()
            self.draw()
    
    def on_mouse_up(self, e):
        self.scroll.is_dragging = False

class Layout:
    def __init__(self):
        self.width_cache = collections.defaultdict(dict) # font: {word: width}
        self._init_state()
        self.style = "roman"
        self.weight = "normal"
        self.size = 12
        self.width = 0
        self.SPACE_WIDTH = get_font(size=self.size, style=self.style, weight=self.weight).measure(" ")
        self.LINESPACE = get_font(size=self.size, style=self.style, weight=self.weight).metrics("linespace")*1.25
        self.current_font = get_font()
        self.align = "left" # center or left
        self.supersub = "normal" # superscript, subscript, or normal
        self.pre = False
    
    def _init_state(self):
        self.display_list = []
        self.line = []
        self.cx, self.cy = MARGINS[0], MARGINS[1]
    
    def calculate(self, tree, width):
        self._init_state()
        self.width = width
        self.recurse(tree)
        self.flush()
        return self.display_list
    
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
            self.cy += self.LINESPACE
        elif tag == "h1":
            self.flush()
            self.cy += self.LINESPACE
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
                    self.word(tree.text, wrap=False)
            else:
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
            
        if wrap and self.cx + w > self.width - MARGINS[2]:
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
        line_length = self.cx - self.SPACE_WIDTH - MARGINS[0]
        metrics = [font.cached_metrics for _, _, font, _ in self.line]
        max_ascent = max(metric["ascent"] for metric in metrics)
        max_descent = max(metric["descent"] for metric in metrics)
        baseline = self.cy + 1.25*max_ascent
        
        # position words so they sit right above the baseline (by their ascent height)
        for x, word, font, supersub in self.line:
            y = self.cy
            if self.align == "center":
                x += (self.width/2)-(line_length/2)
            if supersub == "superscript":
                # raise superscript text by moving it up by half the font's ascent
                y = baseline - (2 * font.cached_metrics["ascent"])
            else:
                y = baseline - font.cached_metrics["ascent"]
            self.display_list.append((x, y, word, font))

        # move cursor below deepest descent
        self.cy = baseline + 1.25*max_descent

        # reset to left
        self.cx = MARGINS[0]
        self.line = []

    def _findsplit(self, parts):
        # binary search for latest possible place to hyphenate word
        l, r = 0, len(parts)-1
        ans = -1
        while l <= r:
            mid = (l + r) // 2
            leftword = ''.join(parts[:mid+1]) + "-"
            w = self.current_font.measure(leftword)

            if self.cx + w <= self.width - MARGINS[2]:
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return ans

if __name__ == "__main__":
    import sys

    command = None
    options = {}
    url = ""
    for arg in sys.argv[1:]:
        if arg in ("-h", "help"):
            print("Usage: python3 browser.py [-rtl, -h] <url>")
        elif arg == "-rtl":
            options["rtl"] = True
        else:
            url = arg
    url = url or "file:///home/yuzu/Documents/browser-dev/hi"
    print(url)
    Browser(options).load(URL(url))
    tkinter.mainloop()