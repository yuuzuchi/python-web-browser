import collections
import tkinter
import tkinter.font
from font_cache import get_font
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

class Text:
    def __init__(self, text):
        self.text = text

class Tag:
    def __init__(self, tag):
        self.tag = tag

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
        self.tokens = []
        self.text_height = 0
        self.rtl = options.get("rtl", False)
        
        self.layout = Layout()
        self.display_list = []
        
    def resize_canvas(self, e):
        self.width = e.width
        self.height = e.height
        self.canvas.config(width=self.width, height=self.height)
        self.display_list = self.layout.calculate(self.tokens, self.width)
        self.text_height = self.display_list[-1][1] + 20 if self.display_list else 0 # height of last object to draw
        self.draw()
    
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
        self.tokens = lex(body)
        self.display_list = self.layout.calculate(self.tokens, self.width)
        self.text_height = self.display_list[-1][1] * 20 if self.display_list else 0# height of last object to draw
        self.draw()
        
    def scrolldown(self, e):
        """Down arrow / Linux mouse wheel down"""
        self.scroll.pos = max(0, self.scroll.pos + SCROLL_STEP \
                              if self.scroll.pos < self.text_height-self.height+MARGINS[3] \
                              else self.text_height-self.height+MARGINS[3])
        self.draw()
    
    def scrollup(self, e):
        """Up arrow / Linux mouse wheel up"""
        self.scroll.pos = self.scroll.pos - SCROLL_STEP if self.scroll.pos > 0 else 0
        self.draw()
        
    def scrolldelta(self, e):
        """Windows / macOS scroll"""
        self.scroll.pos = self.scroll.pos + e.delta if self.scroll.pos > 0 else 0
        self.draw()

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
            self.scroll.pos = max(self.scroll.pos, 0)
            self.scroll.pos = min(self.scroll.pos, self.text_height-self.height+MARGINS[3])
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
    
    def _init_state(self):
        self.display_list = []
        self.line = []
        self.cx, self.cy = MARGINS[0], MARGINS[1]
    
    def calculate(self, tokens, width):
        self._init_state()
        self.width = width
        for tok in tokens:
            self.token(tok)
        self.flush()
        return self.display_list
        
    def token(self, tok):
        if isinstance(tok, Text):
            # halve font size if super/subscript
            size = self.size/2 if self.supersub.startswith("s") else self.size

            # within a tag, the font will stay the same
            self.current_font = get_font(size=size, style=self.style, weight=self.weight)
            for word in tok.text.split():
                self.word(word)
                
        elif tok.tag in ("i", "em"):
            self.style = "italic"
        elif tok.tag in ("/i", "/em"):
            self.style = "roman"
        elif tok.tag in ("b", "strong"):
            self.weight = "bold"
        elif tok.tag in ("/b", "/strong"):
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cy += self.LINESPACE
        elif tok.tag == 'h1 class="title"':
            self.align = "center"
        elif tok.tag == "/h1":
            self.flush()
            self.cy += self.LINESPACE
            self.align = "left"
        elif tok.tag == "sup":
            self.supersub = "superscript"
        elif tok.tag == "sub":
            self.supersub = "subscript"
        elif tok.tag in ("/sup", "/sub"):
            self.supersub = "normal"

    def word(self, word):
        # get width of word for given style and weight
        font_id = self.current_font.id
        
        word_nohyphen = word.replace("\u00AD", "")
        
        if word_nohyphen in self.width_cache[font_id]:
            w = self.width_cache[font_id][word_nohyphen]
        else:
            w = self.current_font.measure(word_nohyphen)
            self.width_cache[font_id][word_nohyphen] = w
            
        if self.cx + w > self.width - MARGINS[2]:
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
                y = baseline - (1.5 * font.cached_metrics["ascent"])
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
            
def lex(body):
    res = []
    buffer = []
    in_tag = False
    i = 0
    while i < len(body):
        c = body[i]
        if c == "&" and not in_tag:
            if body[i+1:i+4] == "lt;":
                c = "<"
                i += 3
            elif body[i+1:i+4] == "gt;":
                c = ">"
                i += 3
            elif body[i+1:i+5] == "shy;":
                c = "\u00AD"
                i += 4
            buffer.append(c)
        elif c == "<":
            in_tag = True
            if buffer:
                res.append(Text(''.join(buffer)))
            buffer = []
        elif c == ">":
            in_tag = False
            res.append(Tag(''.join(buffer)))
            buffer = []
        else:
            buffer.append(c)
        i += 1
    if not in_tag and buffer:
        res.append(Text(''.join(buffer)))
    
    return res

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