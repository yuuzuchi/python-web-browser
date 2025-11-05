import tkinter.font
import binascii

_font_cache = {}

def hash16(s: str) -> int:
    return binascii.crc_hqx(s.encode(), 0)
        
def get_font(family="Segoe UI", size=16, style="roman", weight="normal"):
    key_int = (
        (min(int(size), 255) & 0xFF) |
        (weight=="bold") << 8 |
        (style=="italic") << 9 |
        (hash16(family) & 0xFFFF) << 10
    )
    if key_int not in _font_cache:
        font = tkinter.font.Font(family=family,size=int(size),slant=style,weight=weight)
        font.id = key_int
        font.cached_metrics = font.metrics()
        _font_cache[key_int] = font
    return _font_cache[key_int]