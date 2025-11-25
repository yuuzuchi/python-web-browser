import tkinter
import skia
import time
from font_cache import get_font, get_width
import gi
from gi.repository import Pango, PangoCairo
import cairo
import subprocess, shlex

# results: pango and skia are orders of magnitude faster than tkinter's font.measure, but give inaccurate width numbers
# skia uses pixel font size
# pango falls back to different fonts and applies hinting differently

def get_font_file(font_desc):
    # Construct a pango-style description, e.g. "DejaVu Sans 12"
    cmd = f"fc-match -f \"%{{file}}\" {shlex.quote(font_desc)}"
    out = subprocess.check_output(cmd, shell=True).decode().strip()
    return out

def skia_get_width(text: str, font):
    text_blob = skia.TextBlob.MakeFromString(text, font)
    # Measure width
    bounds = text_blob.bounds()
    return bounds.width()

def pango_measure_width(text: str, font_desc: Pango.FontDescription):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
    cr = cairo.Context(surface)

    layout = PangoCairo.create_layout(cr)
    layout.set_font_description(font_desc)

    layout.set_text(text)

    width, height = layout.get_size()  # Pango units
    return width / Pango.SCALE, height / Pango.SCALE

if __name__ == "__main__":
    # init tkinter root to initialize font cache
    root = tkinter.Tk()
    root.withdraw()
    family = "Liberation Serif"
    size = 140
    font = get_font(family=family, size=size, style="roman", weight="normal")
    print(font.actual())
    print(get_font_file(f"{family} {size}"))
    skia_font = skia.Font(skia.Typeface(font.actual("family")), size)  # skia uses pixels, approximate conversion
    pango_font_desc = Pango.FontDescription()
    pango_font_desc.set_family(font.actual("family"))
    pango_font_desc.set_size(size * Pango.SCALE) 
    iter = 100
   
    # Benchmark Skia
    start_time = time.time()
    for i in range(iter):
        text = "The quick brown fox jumps over the lazy dog" 
        width = skia_get_width(text, skia_font)
    end_time = time.time()
    print(f"Skia: Text width: {width}, Time taken: {end_time - start_time} seconds")

    # Benchmark tkinter
    start_time = time.time()
    for i in range(iter):
        text = "The quick brown fox jumps over the lazy dog" 
        width = font.measure(text)
    end_time = time.time()
    print(f"Tkinter: Text width: {width}, Time taken: {end_time - start_time} seconds")

    # Benchmark Pango
    start_time = time.time()
    for i in range(iter):
        text = "The quick brown fox jumps over the lazy dog" 
        width = pango_measure_width(text, pango_font_desc)
    end_time = time.time()
    print(f"Pango: Text width: {width}, Time taken: {end_time - start_time} seconds")