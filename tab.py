from dataclasses import dataclass
import time
import tkinter
from css_parser import CSSParser, print_rules, style
from html_parser import Element, HTMLParser, Text, print_tree
from layout import MARGINS, DocumentLayout, TextLayout, paint_tree, tree_to_list
from url import URL

@dataclass
class ScrollState:
    is_dragging: bool = False
    drag_offset: int = 0
    pos: int = 0
    bar_y: int = 0
    bar_width: int = MARGINS[4]
    bar_height: int = 0
    velocity: float = 0
    friction: float = 0.7
    step: int = 70
    target_pos: int = 0

class Tab:
    def __init__(self, url: URL, canvas: tkinter.Canvas, tab_height, options: dict={}):
        self.url = url
        self.canvas = canvas
        self.options = options
        self.scroll = ScrollState()
        self.rootnode = []
        self.text_height = 0
        self.tab_height = tab_height
        self.offset = 0
        self.dirty = True # render frame
        
        self.document = None
        self.display_list = []
        self.url = None
        self.history = [url]
        self.forward_history = []
        self.title = "blank"
        self._on_title_change = None
        self._on_open_in_new_tab = None
        
        self.css_parser = CSSParser(open("browser.css").read())
        self.DEFAULT_STYLE_SHEET = self.css_parser.parse(origin_priority=1)
        self.rules = []
        
        self.load(url)
    
    def draw(self):
        self.update_scroll()
        if not self.dirty:
            return
        
        self.canvas.delete("content")
        for cmd in self.display_list:
            if cmd.rect.top > self.scroll.pos + self.tab_height: continue
            if cmd.rect.bottom + MARGINS[3] < self.scroll.pos: continue
            cmd.execute(self.scroll.pos - self.offset, self.canvas, tags=('content'))
        
        self.dirty = False
    
    def load(self, url: URL):
        self.url = url
        body = url.request()
        self.rootnode = HTMLParser(body).parse()

        # css rules
        self.css_parser.reset()
        self.rules = self.DEFAULT_STYLE_SHEET.copy()
        tree_as_list = tree_to_list(self.rootnode, [])
        for node in tree_as_list:
            # external stylesheets
            if isinstance(node, Element) and node.tag == "link" \
                    and node.attributes.get("rel") == "stylesheet" \
                    and "href" in node.attributes:
                style_url = url.resolve(node.attributes['href'])
                try:
                    body = style_url.request()
                    self.rules.extend(self.css_parser.parse(origin_priority=1, s=body))
                except:
                    print("Could not fetch stylesheet from", style_url)

            elif isinstance(node, Text) and node.parent.tag == "title":
                self.title = node.text
                if self._on_title_change:
                    self._on_title_change(self.title)

        start_time = time.perf_counter()
        style(self.rootnode, self.rules, self.css_parser)
        elapsed_time = time.perf_counter() - start_time
        
        self.document = DocumentLayout(self.rootnode, self.canvas)
        # conditional debug output controlled by CLI flags:
        if self.options.get("t", False):
            print(print_tree(self.rootnode, source=True))
        if self.options.get("c", False):
            print_rules(self.rules)
            print(f"style() in{elapsed_time: .6f} seconds, {len(self.rules)} rules")
        print("\nCalculating layout...\n")

        self._layout()
    
    def _layout(self):
        start_time = time.perf_counter()
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        elapsed_time = time.perf_counter() - start_time
        print(f"layout() {self.canvas.winfo_width()}x{self.canvas.winfo_height()} in{elapsed_time: .6f} seconds, {len(self.display_list)} nodes")
        self.text_height = max(self.document.height, 0)
        self.invalidate() 
        
    def navigate(self, url: str, from_user_input: bool = False):       
        url = self.url.resolve(url, from_user_input=from_user_input)
        self.history.append(url)
        self.forward_history = []
        self.load(url)
        self.scroll.pos = self.scroll.target_pos = 0
    
    def go_back(self):
        if self.can_go_back():
            self.forward_history.append(self.history.pop())
            back = self.history[-1]
            self.load(back)
            
    def go_forward(self):
        if self.can_go_forward():
            forward = self.forward_history.pop()
            self.history.append(forward)
            self.load(forward)
        
    def can_go_back(self): return len(self.history) > 1
    def can_go_forward(self): return self.forward_history
        
    def scrolldown(self):
        """Down arrow / Linux mouse wheel down"""
        self.scroll.velocity += 4
        self.scroll.target_pos += self.scroll.step
    
    def scrollup(self):
        """Up arrow / Linux mouse wheel up"""
        self.scroll.velocity -= 4
        self.scroll.target_pos -= self.scroll.step
        
    def scrolldelta(self, delta):
        """Windows / macOS scroll"""
        self.scroll.velocity += self.scroll.step / 2 * delta
        
    def update_scroll(self):
        height = self.tab_height
        
        self.scroll.pos += self.scroll.velocity
        self.scroll.velocity *= self.scroll.friction
        self.scroll.pos += (self.scroll.target_pos - self.scroll.pos) * 0.28

        # snap to 0
        if abs(self.scroll.velocity) < 0.1:
            self.scroll.velocity = 0
        else:
            self.invalidate() # still need to render as long as velocity is nonzero
        if abs(self.scroll.target_pos - self.scroll.pos) < 0.5:
            self.scroll.pos = self.scroll.target_pos
        
        # constrain
        self.scroll.pos = min(self.scroll.pos, self.text_height-height+MARGINS[3])
        self.scroll.pos = max(0, self.scroll.pos)
        self.scroll.target_pos = min(self.scroll.target_pos, self.text_height-height+MARGINS[3])
        self.scroll.target_pos = max(0, self.scroll.target_pos)

    def on_leftmouse_down(self, x, y):
        width = self.canvas.winfo_width()

        # handle scrollbar drag
        if y >= self.scroll.bar_y and y <= self.scroll.bar_y + self.scroll.bar_height and \
                x >= width-self.scroll.bar_width and x < width:
            self.scroll.is_dragging = True
            self.scroll.drag_offset = y - self.scroll.bar_y

        # calculate x, y RELATIVE to scroll
        y += self.scroll.pos
        elt = self.get_element_at_coords(x, y)
        while elt:
            if isinstance(elt, Element) and elt.tag == "a" and "href" in elt.attributes:
                print("Clicked: ", elt.attributes["href"])
                return self.navigate(elt.attributes["href"])
            elt = elt.parent
            
    def on_middlemouse_down(self, x, y):
        y += self.scroll.pos
        elt = self.get_element_at_coords(x, y)
        while elt:
            if isinstance(elt, Element) and elt.tag == "a" and "href" in elt.attributes:
                print("Open in new tab:", elt.attributes["href"])
                url = self.url.resolve(elt.attributes["href"])
                if self._on_open_in_new_tab:
                    return self._on_open_in_new_tab(url)
                
                print("Failed to open in new tab")
            elt = elt.parent
    
    def handle_drag_scroll(self, x, y):
        # scrollbar drag
        if self.scroll.is_dragging:
            bar_y = y - self.scroll.drag_offset
            # invert the drawing formula: scroll.pos = bar_y * text_height / content_height
            self.scroll.target_pos = self.scroll.pos = (self.text_height * bar_y) / self.tab_height

        # absolute scroll (click-to-jump)
        else:
            screen_percent = y / self.tab_height
            self.scroll.target_pos = self.scroll.pos = (self.text_height - self.tab_height) * screen_percent
            self.invalidate()

    def on_mouse_up(self):
        self.scroll.is_dragging = False
        
    def invalidate(self):
        self.dirty = True
        
    def get_element_at_coords(self, x, y):
        objs = [obj for obj in tree_to_list(self.document, [])
                if obj.x <= x < obj.x + obj.width
                and obj.y <= y < obj.y + obj.height]
        
        if not objs: return
        deepest = objs[-1] # most recently painted object is probably the one clicked on
        if isinstance(deepest, TextLayout):
            elt = deepest.node
        else:
            elt = deepest.nodes[-1]
       
        return elt