import tkinter
from html_parser import HTMLParser, print_tree
from url import URL
from dataclasses import dataclass
from layout import DocumentLayout, paint_tree, MARGINS
        
SCROLL_STEP = 60

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
        self.nodes = []
        self.text_height = 0
        self.rtl = options.get("rtl", False)
        
        self.document = None
        self.display_list = []
        
    def resize_canvas(self, e):
        self.ctx.width = e.width
        self.ctx.height = e.height
        self.canvas.config(width=e.width, height=e.height)
        self._layout()
    
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
        self.nodes = HTMLParser(body).parse()
        self.document = DocumentLayout(self.nodes, self.ctx)
        print(print_tree(self.nodes, source=True))
        print("\nCalculating layout...\n")
        self._layout()
    
    def _layout(self):
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.text_height = max(self.document.height, 0)
        print(self.text_height)
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
        self.scroll.pos = min(self.scroll.pos, self.text_height-self.ctx.height+MARGINS[3])
        self.scroll.pos = max(0, self.scroll.pos)

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
            self.scroll.pos = self.text_height * bar_y / self.ctx.height
            self.constrain_scroll()
            self.draw()
    
    def on_mouse_up(self, e):
        self.scroll.is_dragging = False

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
    url = url or "file:///home/yuzu/Documents/browser-dev/parsetest"
    print(url)
    Browser(options).load(URL(url))
    tkinter.mainloop()