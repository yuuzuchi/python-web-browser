from layout.box import Box


class InlineBox(Box):
    """
    https://drafts.csswg.org/css2/#inline-boxes
    **NOTE:**: technically not always a "box".

    inline-level box can be either an **inline box** OR **atomic inline-level box**.
    **inline box**: contents of this block are formatted inline, meaning the box could be split when line wrapping.
        - not guaranteed to be rectangular, so does not respect width/height properties
    **atomic inline level box**: contents of this box are formatted as a block, cannot be split.
        - if the box doesn't fit on the line, move the entire box to the next line
        - respects width/height properties
    """

    def __init__(self, node, parent):
        super().__init__(node, parent, None)

    def __repr__(self):
        tag = getattr(self.node, "tag", None)
        return f"<InlineBox {tag} children={len(self.children)}>"
