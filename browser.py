import tkinter
from url import URL
from dataclasses import dataclass

WIDTH, HEIGHT = 1280, 720
HSTEP, VSTEP = 10, 13
SCROLL_STEP = 60

@dataclass
class scrollstate:
    is_dragging: bool = False
    drag_offset: int = 0
    pos: int = 0
    bar_y: int = 0
    bar_height: int = 0

class Browser:
    def __init__(self):
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
        self.text = ""
        self.text_height = 0
        
    def resize_canvas(self, e):
        self.width = e.width
        self.height = e.height
        self.canvas.config(width=self.width, height=self.height)
        self.display_list = layout(self.text, self.width)
        self.text_height = self.display_list[-1][1] if self.display_list else 0 # height of last object to draw
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        self.draw_scrollbar()
        for x, y, c in self.display_list:
            if y > self.scroll.pos + self.height: continue
            if y + VSTEP < self.scroll.pos: continue
            self.canvas.create_text(x, y - self.scroll.pos, text=c)
            
    def draw_scrollbar(self):
        if self.height >= self.text_height:
            return
        self.canvas.create_rectangle(self.width-10, 0, self.width, self.height, width=0, fill="#cccccc")
        self.scroll.bar_height = self.height**2 / self.text_height
        self.scroll.bar_y = self.scroll.pos*self.height / self.text_height
        self.canvas.create_rectangle(self.width-10, self.scroll.bar_y, self.width, self.scroll.bar_y+self.scroll.bar_height, width=0, fill="#aaaaaa")
    
    def load(self, url: URL):
        body = url.request()
        self.text = lex(body)
        self.display_list = layout(self.text, self.width)
        self.text_height = self.display_list[-1][1] if self.display_list else 0# height of last object to draw
        self.draw()
        
    def scrolldown(self, e):
        """Down arrow / Linux mouse wheel down"""
        self.scroll.pos = max(0, self.scroll.pos + SCROLL_STEP if self.scroll.pos < self.text_height-self.height+VSTEP else self.text_height-self.height+VSTEP)
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
            self.scroll.pos = min(self.scroll.pos, self.text_height-self.height+VSTEP)
            self.draw()
    
    def on_mouse_up(self, e):
        self.scroll.is_dragging = False
        
def layout(text, width):
    display_list = []
    cx, cy = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cx = HSTEP
            cy += VSTEP*1.5
            continue
        
        display_list.append((cx, cy, c))
        cx += HSTEP
        if cx >= width-HSTEP:
            cy += VSTEP
            cx = HSTEP
    return display_list

def lex(body):
    text = []
    in_tag = False
    i = 0
    while i < len(body):
        c = body[i]
        if c == "<": in_tag = True
        elif c == ">": in_tag = False
        elif not in_tag:
            if c == "&":
                if body[i+1:i+4] == "lt;":
                    c = "<"
                elif body[i+1:i+4] == "gt;":
                    c = ">"
                i += 3
            text.append(c)
        i += 1
    
    return ''.join(text)

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "file:///home/yuzu/Documents/browser-dev/hi"
    Browser().load(URL(url))
    tkinter.mainloop()