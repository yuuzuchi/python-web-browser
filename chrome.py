from draw import *
from font_cache import get_font, get_width
from url import URL
from browser import Browser

class Chrome:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.font = get_font(size=16, weight="normal", style="roman")
        self.font_height = self.font.cached_metrics["linespace"]

        self.padding = 5
        self.tabbar_top = 0
        self.tabbar_bottom = self.font_height + 2*self.padding
        self.urlbar_top = self.tabbar_bottom
        self.urlbar_bottom = self.urlbar_top + \
        self.font_height + 2*self.padding
        self.bottom = self.urlbar_bottom
        
        self.focus = None
        self.address_bar = ""

        self.PLUS_WIDTH = self.font.measure("+") + 2*self.padding
        self.newtab_rect = Rect(self.padding, self.padding, self.padding+self.PLUS_WIDTH, self.padding+self.font_height)

        self.NAV_WIDTH = self.font.measure("<") + 2*self.padding
        self.back_rect = Rect(self.padding, self.urlbar_top+self.padding, 
                              self.padding+self.NAV_WIDTH, self.urlbar_bottom-self.padding)
        self.forward_rect = Rect(self.back_rect.right+self.padding, self.urlbar_top+self.padding, 
                              self.back_rect.right+self.padding+self.NAV_WIDTH, self.urlbar_bottom-self.padding)
        self.address_rect = Rect(self.forward_rect.right+self.padding, self.urlbar_top+self.padding, 
                                 self.browser.canvas.winfo_width()-self.padding, self.urlbar_bottom-self.padding)

    def resize(self):
        self.address_rect.right = self.browser.canvas.winfo_width()-self.padding
        
    def tab_rect(self, i):
        tabs_start = self.newtab_rect.right + self.padding
        tab_width = self.font.measure("Tab X") + 2*self.padding
        return Rect(
            tabs_start + tab_width*i, self.tabbar_top,
            tabs_start + tab_width*(i+1), self.tabbar_bottom)
        
    def click(self, x, y):
        self.focus = None
        if self.newtab_rect.contains_point(x, y):
            self.browser.new_tab(URL("https://browser.engineering"))
        elif self.back_rect.contains_point(x, y):
            self.browser.active_tab.go_back()
        elif self.forward_rect.contains_point(x, y):
            self.browser.active_tab.go_forward()
        elif self.address_rect.contains_point(x, y):
            self.focus = "address bar"
            self.address_bar = ""
        else:
            for i, tab in enumerate(self.browser.tabs):
                if self.tab_rect(i).contains_point(x, y):
                    self.set_tab(tab)
                    break
                
    def middleclick(self, x, y):
        self.focus = None
        for i, tab in enumerate(self.browser.tabs):
            if self.tab_rect(i).contains_point(x, y):
                self.browser.tabs.pop(i)
                if len(self.browser.tabs) == 0:
                    blank = URL("about:blank")
                    self.set_tab(blank)
                elif i != len(self.browser.tabs):
                    # select tab to the right
                    self.set_tab(self.browser.tabs[i-1])
                else:
                    self.set_tab(self.browser.tabs[-1])
                break
            
    def set_tab(self, tab):
        self.browser.set_tab(tab)

    def keypress(self, char):
        if self.focus == "address bar":
            self.address_bar += char
    
    def enter(self):
        if self.focus == "address bar":
            self.browser.active_tab.navigate(self.address_bar, from_user_input=True)
            self.focus = None
    
    def backspace(self):
        if self.focus == "address bar":
            self.address_bar = self.address_bar[:-1]
            
    def paint(self):
        cmds = []
        
        # white rectangle behind UI
        cmds.append(DrawRect(
            Rect(0, 0, self.browser.canvas.winfo_width(), self.bottom), "white"))
        
        # black line separating chrome and content
        cmds.append(DrawLine(
            0, self.bottom, self.browser.canvas.winfo_width(), self.bottom, "black", 1))
        
        # new tab button
        cmds.append(DrawText(self.newtab_rect.left+self.padding, self.newtab_rect.top, "+", self.PLUS_WIDTH, self.font, "black"))
        cmds.append(DrawOutline(self.newtab_rect, "black", 1))
        
        cmds.extend(self.paint_tabs())

        # navigation buttons
        back_color = "black" if self.browser.active_tab.can_go_back() else "gray"
        forward_color = "black" if self.browser.active_tab.can_go_forward() else "gray"
        
        cmds.append(DrawOutline(self.back_rect, back_color, 1))
        cmds.append(DrawText(self.back_rect.left + self.padding, self.back_rect.top, "<", self.NAV_WIDTH, self.font, back_color))
        cmds.append(DrawOutline(self.forward_rect, forward_color, 1))
        cmds.append(DrawText(self.forward_rect.left + self.padding, self.forward_rect.top, ">", self.NAV_WIDTH, self.font, forward_color))
        
        cmds.extend(self.paint_addressbar())
        cmds.append(DrawOutline(self.address_rect, "black", 1))
                
        return cmds
    
    def paint_tabs(self):
        out = []
        for i, tab in enumerate(self.browser.tabs):
            bounds = self.tab_rect(i)
            out.append(DrawLine(
                bounds.left, 0, bounds.left, bounds.bottom, "black", 1))
            out.append(DrawLine(
                bounds.right, 0, bounds.right, bounds.bottom, "black", 1))
            out.append(DrawText(
                bounds.left+self.padding, bounds.top+self.padding, f"Tab {i}", self.PLUS_WIDTH, self.font, "black"))
            
            if tab == self.browser.active_tab:
                out.append(DrawLine(
                    0, bounds.bottom, bounds.left, bounds.bottom, "black", 1))
                out.append(DrawLine(
                    bounds.right, bounds.bottom, self.browser.canvas.winfo_width(), bounds.bottom, "black", 1))
        return out
    
    def paint_addressbar(self):
        out = []
        if self.focus == "address bar":
            w = get_width(self.address_bar, self.font)
            out.append(DrawText(
                self.address_rect.left + self.padding,
                self.address_rect.top,
                self.address_bar, w, self.font, "black"))
            
            out.append(DrawLine(
                self.address_rect.left + self.padding + w,
                self.address_rect.top,
                self.address_rect.left + self.padding + w,
                self.address_rect.bottom,
                "red", 1))
        else:
            url = str(self.browser.active_tab.url)
            w = get_width(url, self.font)
            out.append(DrawText(
                self.address_rect.left + self.padding,
                self.address_rect.top,
                url, w, self.font, "black")) 
        
        return out