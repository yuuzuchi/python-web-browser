import re
import tkinter
from font_cache import get_font, get_width
from layout import BlockLayout, BreakLayout, Layout, LineLayout, TextFragment, AnonymousLayout, flatten

class BlockFormattingContext():
    def __init__(self, block: Layout):
        self.block = block
        self.style = block.computed_style()
        
    def format(self):
        self.block.x = self.block.parent.x
        self.block.width = self.block.parent.width
        self.block.y = self.block.previous.y + self.block.previous.height if self.block.previous else self.block.parent.y
        self.block.line_boxes = []  # Reset line_boxes from previous layout pass
        
        if self.block.has_inline_children():
            # inline formatter over entire block
            # (if has inline children, entire block must ONLY contain inline children)
            inline = InlineFormattingContext(self.block)
            self.block.line_boxes = inline.format() or []
            self.block.height = sum([line.height for line in self.block.line_boxes])
            return

        width = self.style.get("width", "auto")
        height = self.style.get("height", "auto")
        if width.endswith("px"):
            self.block.width = int(width[:-2])
        if height.endswith("px"):
            self.block.height = int(height[:-2])
        
        # format block children
        for child in self.block.children:
            assert isinstance(child, (BlockLayout, AnonymousLayout))
            ctx = BlockFormattingContext(child)
            ctx.format()

        self.block.height = sum([child.height for child in self.block.children])
    
class InlineFormattingContext():
    def __init__(self, block: Layout):
        self.block = block
        self.style = block.computed_style()
        
        self.x = self.block.parent.x
        self.y = self.block.previous.y + self.block.previous.height if self.block.previous else self.block.parent.y
        self.available_width = self.block.parent.width
        self.cx = 0
        self.cy = 0
        self.curr_line = self.new_line(self.block.node)
        self.out = []
        
    def new_line(self, DOM_reference_node):
        line = LineLayout(DOM_reference_node)
        line.x = self.x
        line.y = self.y + self.cy
        line.width = self.available_width
        return line        
    
    def format(self):
        """Given an inline block filled with TextLayout or LineLayout, returns a list containing LineLayout and/or BreakLayouts"""
        # TODO: prevent BlockLayout from creating blank LineLayouts in the first place
        if not self.block.children:
            self.block.height = 0
            return []
        
        for layout in flatten(self.block.children):
            style = layout.computed_style()
            if isinstance(layout, BreakLayout):
                self.flush_line(layout.node)
            else:
                font = self.get_font(style)
                color = style.get("color")
                
                # split on newlines
                if style.get("white-space") == "pre":
                    parts = layout.text_run.split("\n")
                    for i, line in enumerate(parts):
                        self.add_fragment_to_line(line, font, color, layout, pre=True)
                        if i < len(parts) - 1:
                            self.flush_line(layout.node)
                    continue
                
                # split into fragments, add each fragment to curr_line while checking for wrap
                clean_text = self.normalize_text(layout.text_run)
                fragments = clean_text.split(" ")
                for i, fragment in enumerate(fragments):
                    end = "" if i == len(fragments)-1 else " "
                    self.add_fragment_to_line(fragment, font, color, layout, pre=False, end=end)

        if self.curr_line.children:
            self.flush_line(self.block.node)
            
        return self.out
        
    def add_fragment_to_line(self, fragment: str, font: tkinter.font.Font, color: str, layout_object, pre=False, end=" "):
        # remove whitespace at the beginning of boxes
        if not pre and fragment == "" and self.cx == 0:
            return
        fragment_without_hyphen = fragment.replace("\u00AD", "")
        space_w = 0 if pre or end == "" else get_width(end, font)
        w = get_width(fragment_without_hyphen, font) + space_w
        
        if not pre and self.cx + w > self.available_width:
            if "\u00AD" not in fragment:
                self.flush_line(layout_object.node)
            else:
                parts = fragment.split("\u00AD")
                idx = self.findsplit(parts, font)
                righthalf = "\u00AD".join(parts[idx+1:])
                lefthalf = ''.join(parts[:idx+1]) + '-' if idx != -1 else ''
                
                self.curr_line.children.append(TextFragment(layout_object, lefthalf, self.x + self.cx, self.y + self.cy, w, font, color))
                self.flush_line(layout_object.node)
                self.add_fragment_to_line(righthalf, font, color, layout_object, pre=pre)
                return

        frag = TextFragment(layout_object, fragment_without_hyphen, self.x + self.cx, self.y + self.cy, w, font, color)
        self.cx += w
        self.curr_line.children.append(frag)
        
    # align text vertically
    def flush_line(self, DOM_node_reference):
        self.cx = 0
        if not self.curr_line.children:
            self.curr_line.height = 0
            
        elif len(self.curr_line.children) == 1 and isinstance(self.curr_line.children[0], BreakLayout):
            br_font = self.get_font(self.curr_line.children[0].computed_style())
            self.curr_line.height = br_font.cached_metrics["linespace"]
        else:
            max_ascent = max([fragment.font.cached_metrics["ascent"] for fragment in self.curr_line.children])
            max_descent = max([fragment.font.cached_metrics["descent"] for fragment in self.curr_line.children])
            baseline = self.curr_line.y + 1.25 * max_ascent
            for fragment in self.curr_line.children:
                fragment.y = baseline - fragment.font.cached_metrics["ascent"]
            self.curr_line.height = 1.25 * (max_ascent + max_descent)

        self.cy += self.curr_line.height
        self.out.append(self.curr_line)
        self.curr_line = self.new_line(DOM_node_reference)
            
    # get cached font from style
    def get_font(self, style: dict):
        family = style.get("font-family")
        weight = style.get("font-weight", 16)
        fontstyle = style.get("font-style", "roman")
        if fontstyle == "normal": fontstyle = "roman"
        size = int(float(style["font-size"][:-2]) * .75)
        return get_font(family=family, size=size, weight=weight, style=fontstyle)

    # binary search for latest possible place to hyphenate word
    def findsplit(self, parts, font):
        l, r = 0, len(parts)-1
        ans = -1
        while l <= r:
            mid = (l + r) // 2
            leftword = ''.join(parts[:mid+1]) + "-"
            w = get_width(leftword, font)

            if self.cx + w <= self.available_width:
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return ans
    
    def normalize_text(self, text):
        return re.sub(r'\s+', ' ', text)