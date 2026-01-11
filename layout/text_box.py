from layout.box import Box


class TextBox(Box):
    def __init__(self, node, text_run, parent):
        super().__init__(node, parent, None)
        self.text_run = text_run

    def __repr__(self):
        txt = (
            (self.text_run[:16] + "...")
            if self.text_run and len(self.text_run) > 16
            else (self.text_run or "")
        )
        return f"<TextBox '{txt}' x={self.x} y={self.y} w={self.width} h={self.height}>"
