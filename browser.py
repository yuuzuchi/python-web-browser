import tkinter
from url import URL

WIDTH, HEIGHT = 1280, 720
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 60

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
        
        self.scroll = 0
        self.text = ""
        self.text_height = 0
        
    def resize_canvas(self, e):
        self.width = e.width
        self.height = e.height
        #print(WIDTH, HEIGHT)
        self.canvas.config(width=self.width, height=self.height)
        self.display_list = layout(self.text, self.width)
        self.text_height = self.display_list[-1][1] # height of last object to draw
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height)
        for x, y, c in self.display_list:
            if y > self.scroll + self.height: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)
    
    def load(self, url: URL):
        body = url.request()
        self.text = lex(body)
        self.display_list = layout(self.text, self.width)
        self.text_height = self.display_list[-1][1] # height of last object to draw
        self.draw()
        
    def scrolldown(self, e):
        """Down arrow / Linux mouse wheel down"""
        self.scroll = self.scroll + SCROLL_STEP if self.scroll < self.text_height-self.height+VSTEP else self.text_height-self.height+VSTEP
        self.draw()
    
    def scrollup(self, e):
        """Up arrow / Linux mouse wheel up"""
        self.scroll = self.scroll - SCROLL_STEP if self.scroll > 0 else 0
        self.draw()
        
    def scrolldelta(self, e):
        """Windows / macOS scroll"""
        self.scroll = self.scroll + e.delta if self.scroll > 0 else 0
        self.draw()
        
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