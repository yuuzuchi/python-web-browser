import tkinter
from html_parser import Element, HTMLParser, print_tree
from url import URL
from dataclasses import dataclass
from layout import DocumentLayout, paint_tree, tree_to_list, MARGINS
from css_parser import CSSParser, style, print_rules
import time
        
DEFAULT_STYLE_SHEET = CSSParser(open("browser.css").read()).parse()

@dataclass
class WindowContext:
    width: int
    height: int

@dataclass
class scrollstate:
    is_dragging: bool = False
    drag_offset: int = 0
    pos: int = 0
    bar_y: int = 0
    bar_height: int = 0
    velocity: float = 0
    friction: float = 0.7
    step: int = 70
    target_pos: int = 0

class Browser:
    def __init__(self, options: dict={}):
        """Options:
        - rtl: bool, Right to Left text direction rendering
        - s <width>x<height>"""
        dimensions = [int(val) for val in options.get("s", "1280x720").split("x")]
        self.ctx = WindowContext(dimensions[0], dimensions[1])
        self.window = tkinter.Tk()
        self.window.configure(bg="white")
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.ctx.width,
            height=self.ctx.height,
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
        self.rootnode = []
        self.text_height = 0
        self.rtl = options.get("rtl", False)
        
        self.document = None
        self.display_list = []

        # keep CLI flags accessible to other methods
        self.options = options
        
    def resize_canvas(self, e):
        self.ctx.width = e.width
        self.ctx.height = e.height
        self.canvas.config(width=e.width, height=e.height)
        self._layout()
        
    def update(self):
        self.update_scroll()
        self.draw()
        
        self.window.after(8, self.update)
    
    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll.pos + self.ctx.height: continue
            if cmd.bottom + MARGINS[3] < self.scroll.pos: continue
            cmd.execute(self.scroll.pos, self.canvas)
        self.draw_scrollbar()
            
    def draw_scrollbar(self):
        if self.ctx.height >= self.text_height:
            return
        self.canvas.create_rectangle(self.ctx.width-10, 0, self.ctx.width, self.ctx.height, width=0, fill="#cccccc")
        self.scroll.bar_height = self.ctx.height**2 / self.text_height
        self.scroll.bar_y = self.scroll.pos*self.ctx.height / self.text_height
        self.canvas.create_rectangle(self.ctx.width-10, self.scroll.bar_y, self.ctx.width, self.scroll.bar_y+self.scroll.bar_height, width=0, fill="#aaaaaa")
    
    def load(self, url: URL):
        body = url.request()
        self.rootnode = HTMLParser(body).parse()

        # css rules
        rules = DEFAULT_STYLE_SHEET.copy()
        tree_as_list = tree_to_list(self.rootnode, [])
        for i, node in enumerate(tree_as_list):
            # external stylesheets
            if isinstance(node, Element) and node.tag == "link" \
                    and node.attributes.get("rel") == "stylesheet" \
                    and "href" in node.attributes:
                style_url = url.resolve(node.attributes['href'])
                try:
                    body = style_url.request()
                    rules.extend(CSSParser(body).parse())
                except:
                    print("Could not fetch stylesheet from", body)

            # style tag stylesheets
            if i < len(tree_as_list)-1 and isinstance(node, Element) and node.tag == "style":
                try:
                    rules.extend(CSSParser(tree_as_list[i+1].text).parse())
                except:
                    print("inline style", tree_as_list[i+1], "could not be parsed")

        start_time = time.perf_counter()
        style(self.rootnode, rules)
        elapsed_time = time.perf_counter() - start_time
        self.document = DocumentLayout(self.rootnode, self.ctx)
        # conditional debug output controlled by CLI flags:
        if self.options.get("t", False):
            print(print_tree(self.rootnode, source=True))
        if self.options.get("c", False):
            print_rules(rules)
            print(f"style() in{elapsed_time: .6f} seconds, {len(rules)} rules")
        print("\nCalculating layout...\n")
        self._layout()
        self.update()
    
    def _layout(self):
        start_time = time.perf_counter()
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        elapsed_time = time.perf_counter() - start_time
        print(f"layout() {self.ctx.width}x{self.ctx.height} in{elapsed_time: .6f} seconds, {len(self.display_list)} nodes")
        self.text_height = max(self.document.height, 0)
        
    def scrolldown(self, e):
        """Down arrow / Linux mouse wheel down"""
        self.scroll.velocity += 4
        self.scroll.target_pos += self.scroll.step
    
    def scrollup(self, e):
        """Up arrow / Linux mouse wheel up"""
        self.scroll.velocity -= 4
        self.scroll.target_pos -= self.scroll.step
        
    def scrolldelta(self, e):
        """Windows / macOS scroll"""
        self.scroll.velocity += self.scroll.step / 2 * e.delta
        
    def update_scroll(self):
        self.scroll.pos += self.scroll.velocity
        self.scroll.velocity *= self.scroll.friction
        self.scroll.pos += (self.scroll.target_pos - self.scroll.pos) * 0.28

        # snap to 0
        if abs(self.scroll.velocity) < 0.1:
            self.scroll.velocity = 0
        if abs(self.scroll.target_pos - self.scroll.pos) < 0.5:
            self.scroll.pos = self.scroll.target_pos
        
        # constrain
        self.scroll.pos = min(self.scroll.pos, self.text_height-self.ctx.height+MARGINS[3])
        self.scroll.pos = max(0, self.scroll.pos)
        self.scroll.target_pos = min(self.scroll.target_pos, self.text_height-self.ctx.height+MARGINS[3])
        self.scroll.target_pos = max(0, self.scroll.target_pos)

    def on_mouse_down(self, e):
        # handle scrollbar drag
        if e.y >= self.scroll.bar_y and e.y <= self.scroll.bar_y + self.scroll.bar_height and \
                e.x >= self.ctx.width-10 and e.x < self.ctx.width:
            self.scroll.is_dragging = True
            self.scroll.drag_offset = e.y - self.scroll.bar_y
    
    def on_mouse_drag(self, e):
        # scrollbar drag
        if self.scroll.is_dragging:
            bar_y = e.y - self.scroll.drag_offset
            self.scroll.target_pos = self.scroll.pos = self.text_height * bar_y / self.ctx.height

        # absolute scroll
        else:
            screen_percent = e.y / self.ctx.height
            self.scroll.target_pos = self.scroll.pos = (self.text_height - self.ctx.height) * screen_percent

    def on_mouse_up(self, e):
        self.scroll.is_dragging = False

if __name__ == "__main__":
    import sys

    command = None
    options = {}
    url = ""
    for arg in sys.argv[1:]:
        if arg in ("-h", "help"):
            print("Usage: python3 browser.py [-rtl] [-c] [-t] [-h] <url>")
        elif arg == "-rtl":
            options["rtl"] = True
        elif arg == "-c":
            options["c"] = True
        elif arg == "-t":
            options["t"] = True
        else:
            url = arg
    url = url or "file:///home/yuzu/Documents/browser-dev/parsetest"
    print(url)
    Browser(options).load(URL(url))
    tkinter.mainloop()