class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def contains_point(self, x, y):
        return x >= self.left and x < self.right and y >= self.top and y < self.bottom

    def __repr__(self):
        return f"Rect(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


class DrawText:
    def __init__(self, x1, y1, text, width, font, color):
        self.top = y1
        self.left = x1
        self.text = text
        self.font = font
        self.color = color
        self.bottom = y1 + font.cached_metrics["linespace"]
        self.rect = Rect(x1, y1, x1 + width, self.bottom)

    def execute(self, scroll, canvas, tags=()):
        canvas.create_text(
            self.left,
            self.top - scroll,
            text=self.text,
            font=self.font,
            fill=self.color,
            anchor="nw",
            tags=tags,
        )

    def __repr__(self):
        txt = (
            (self.text[:30] + "...")
            if self.text and len(self.text) > 30
            else (self.text or "")
        )
        width = self.rect.right - self.rect.left
        return f"DrawText(text='{txt}', x={self.left}, y={self.top}, w={width}, color={self.color})"


class DrawRect:
    def __init__(self, rect: Rect, color):
        self.rect = rect
        self.color = color

    def execute(self, scroll, canvas, tags=()):
        canvas.create_rectangle(
            self.rect.left,
            self.rect.top - scroll,
            self.rect.right,
            self.rect.bottom - scroll,
            width=0,
            fill=self.color,
            tags=tags,
        )

    def __repr__(self):
        return f"DrawRect(rect={self.rect}, color={self.color})"


class DrawOutline:
    def __init__(self, rect: Rect, color, thickness):
        self.rect = rect
        self.color = color
        self.thickness = thickness

    def execute(self, scroll, canvas, tags=()):
        canvas.create_rectangle(
            self.rect.left,
            self.rect.top - scroll,
            self.rect.right,
            self.rect.bottom - scroll,
            width=self.thickness,
            outline=self.color,
            tag=tags,
        )

    def __repr__(self):
        return f"DrawOutline(rect={self.rect}, color={self.color}, thickness={self.thickness})"


class DrawLine:
    def __init__(self, x1, y1, x2, y2, color, thickness):
        self.rect = Rect(x1, y1, x2, y2)
        self.color = color
        self.thickness = thickness

    def execute(self, scroll, canvas, tags):
        canvas.create_line(
            self.rect.left,
            self.rect.top - scroll,
            self.rect.right,
            self.rect.bottom - scroll,
            fill=self.color,
            width=self.thickness,
            tag=tags,
        )

    def __repr__(self):
        return f"DrawLine(x1={self.rect.left}, y1={self.rect.top}, x2={self.rect.right}, y2={self.rect.bottom}, color={self.color}, thickness={self.thickness})"
