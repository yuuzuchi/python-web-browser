import tkinter.font

_font_cache = {}
        
def get_font(size=16, style="roman", weight="normal"):
    key_int = (
        (min(size*2, 255) & 0xFF) |
        (weight=="bold") << 8 |
        (style=="italic") << 9
    )
    if key_int not in _font_cache:
        font = tkinter.font.Font(size=size,slant=style,weight=weight)
        font.id = key_int
        font.cached_metrics = font.metrics()
        _font_cache[key_int] = font
    return _font_cache[key_int]