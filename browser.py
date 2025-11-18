import tkinter
from tab import Tab
from draw import *
from url import URL

class Browser:
    def __init__(self, options: dict={}):
        """Options:
        - rtl: bool, Right to Left text direction rendering
        - s <width>x<height>"""
        dimensions = [int(val) for val in options.get("s", "1280x720").split("x")]
        print(dimensions)
        self.window = tkinter.Tk()
        self.window.configure(bg="white")
        self.canvas = tkinter.Canvas(self.window,
                                     width=dimensions[0], height=dimensions[1],
                                     bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.window.bind("<Key>", self.handle_key)
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Return>", self.handle_enter)
        self.window.bind("<BackSpace>", self.handle_backspace)
        self.window.bind("<Button-4>", self.scrollup)
        self.window.bind("<Button-5>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.scrolldelta)
        self.window.bind("<Button-1>", self.on_mouse_down)
        self.window.bind("<Button-2>", self.on_middlemouse_down)
        self.window.bind("<B1-Motion>", self.on_mouse_drag)
        self.window.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # keep CLI flags accessible to other methods
        self.rtl = options.get("rtl", False) # currently broken sowwy
        self.options = options
        
        self.drawing = False # running draw loop
        self.active_tab = None
        self.tabs = []
        
        from chrome import Chrome
        self.chrome = Chrome(self)

    def new_tab(self, url):
        new_tab = Tab(self.canvas, self.canvas.winfo_height()-self.chrome.bottom, options=self.options)
        new_tab.load(url)
        # set tab's callbacks
        new_tab._on_title_change = self.rename_window
        new_tab._on_open_in_new_tab = self.new_tab
        self.tabs.append(new_tab)
        self.active_tab = new_tab
        self.start()
        self.set_tab(new_tab)

    def draw(self):
        self.active_tab.tab_height = self.canvas.winfo_height()-self.chrome.bottom
        self.active_tab.offset = self.chrome.bottom
        
        self.active_tab.draw()
        
        self.canvas.delete("scrollbar")
        self.draw_scrollbar()

        self.canvas.delete("chrome")
        for cmd in self.chrome.paint():
            cmd.execute(0, self.canvas, tags=('chrome'))
        
    def start(self):
        if self.drawing: 
            return
        self.drawing = True
        self.update()

    def update(self):
        if not self.drawing:
            return
        self.draw()
        self.window.after(8, self.update)
        
    def resize_canvas(self, e):
        self.canvas.config(width=e.width, height=e.height)
        self.active_tab._layout()
        self.chrome.resize()
        
    def rename_window(self, title):
        self.window.title(title)
        
    def set_tab(self, tab: Tab):
        self.active_tab = tab
        self.active_tab.invalidate() # request one draw frame
        if tab:
            self.rename_window(tab.title)

    def draw_scrollbar(self):
        if not self.active_tab:
            return 
        # get scrollbar properties from current tab
        scroll = self.active_tab.scroll
        text_height = self.active_tab.text_height
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()-self.chrome.bottom

        # hide scrollbar if page fits in view
        if height >= text_height:
            return
        
        self.canvas.create_rectangle(
            width-scroll.bar_width, self.chrome.bottom, 
            width, height+self.chrome.bottom, width=0, fill="#cccccc", tags=('scrollbar'))
        
        scroll.bar_height = height**2 / text_height
        scroll.bar_y = (scroll.pos * height) / text_height
        self.canvas.create_rectangle(
            width-scroll.bar_width, self.chrome.bottom + scroll.bar_y,
            width, self.chrome.bottom + scroll.bar_y + scroll.bar_height, width=0, fill="#aaaaaa", tags=('scrollbar'))
        
    # event handlers    
    
    def scrolldown(self, e): self.active_tab.scrolldown()
    def scrollup(self, e): self.active_tab.scrollup()
    def scrolldelta(self, e): self.active_tab.scrolldelta(e.delta)
    def on_mouse_drag(self, e): self.active_tab.handle_drag_scroll(e.x, e.y - self.chrome.bottom)
    def on_mouse_up(self, e): self.active_tab.on_mouse_up()
    def on_mouse_down(self, e): 
        # check clicking on other tabs
        if e.y < self.chrome.bottom:
            self.chrome.click(e.x, e.y)
        else:
            # coords relative to tab
            tab_y = e.y - self.chrome.bottom
            self.active_tab.on_leftmouse_down(e.x, tab_y)
            
    def on_middlemouse_down(self, e): 
        # check clicking on tabs
        if e.y < self.chrome.tabbar_bottom:
            self.chrome.middleclick(e.x, e.y)
        else:
            # coords relative to tab
            tab_y = e.y - self.chrome.bottom
            self.active_tab.on_middlemouse_down(e.x, tab_y)

    def handle_key(self, e):
        if len(e.char) == 0: return
        if not (0x20 <= ord(e.char) < 0x7f): return
        self.chrome.keypress(e.char)
            
    def handle_enter(self, e): self.chrome.enter()
    def handle_backspace(self, e): self.chrome.backspace()

if __name__ == "__main__":
    import sys

    command = None
    options = {}
    url = ""
    for arg in sys.argv[1:]:
        if arg in ("-h", "help"):
            print("Usage: python3 browser.py [-rtl] [-c] [-t] [-h] [<url> | test]")
        elif arg == "-rtl":
            options["rtl"] = True
        elif arg == "-c":
            options["c"] = True
        elif arg == "-t":
            options["t"] = True
        elif arg == "test":
            url = "file:///home/yuzu/Documents/browser-dev/parsetest"
        else:
            url = arg
    if url:
        browser = Browser(options)
        browser.new_tab(URL(url))
        tkinter.mainloop()
    else:
        print("Usage: python3 browser.py [-rtl] [-c] [-t] [-h] [<url> | test]")
