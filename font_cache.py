import collections
import tkinter.font
import binascii

# try: 
#     import gi
#     gi.require_version('Pango', '1.0')
#     gi.require_version('PangoCairo', '1.0')
#     from gi.repository import Pango, PangoCairo
#     import cairo
#     _PANGO_AVAILABLE = True
# except ImportError:
#     _PANGO_AVAILABLE = False
_PANGO_AVAILABLE = False

_font_cache = {}
_width_cache = collections.defaultdict(dict)

def get_width(word, font):
    font_id = font.id
    if word in _width_cache[font_id]:
        return _width_cache[font_id][word]
    else:
        if _PANGO_AVAILABLE and hasattr(font, "pango_font_desc"):
            w, _ = pango_measure_text(word, font.pango_font_desc)
        else:
            w = font.measure(word)
        _width_cache[font_id][word] = w
        return w

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
        if _PANGO_AVAILABLE:
            pango_font_desc = Pango.FontDescription()
            pango_font_desc.set_family(family)
            pango_font_desc.set_size(size * Pango.SCALE)
            pango_font_desc.set_weight(
                Pango.Weight.BOLD if weight == "bold" else Pango.Weight.NORMAL)
            pango_font_desc.set_style(
                Pango.Style.ITALIC if style == "italic" else Pango.Style.NORMAL)
            font.pango_font_desc = pango_font_desc
        _font_cache[key_int] = font
        
    return _font_cache[key_int]

def pango_measure_text(text: str, font_desc):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    cr = cairo.Context(surface)

    layout = PangoCairo.create_layout(cr)
    layout.set_font_description(font_desc)

    layout.set_text(text)

    width, height = layout.get_size()  # Pango units
    return width / Pango.SCALE, height / Pango.SCALE