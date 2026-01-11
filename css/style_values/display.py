from __future__ import annotations
from css.enums import DisplayBox
from css.enums import DisplayInternal
from css.enums import DisplayLegacy
from css.enums import DisplayInside
from css.enums import DisplayOutside
from dataclasses import dataclass
from css.style_values.base import StyleValue
from css.lexer import Token, Tok
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from css.lexer import Token


@dataclass
class DisplayValue(StyleValue):
    display: Display

    def to_token(self) -> Token:
        return Token(Tok.IDENT, str(self.display))


class Display:
    def __init__(
        self,
        outside: Optional[DisplayOutside] = None,
        inside: Optional[DisplayInside] = None,
        is_list_item: bool = False,
        legacy: Optional[DisplayLegacy] = None,
        internal: Optional[DisplayInternal] = None,
        box: Optional[DisplayBox] = None,
    ):
        self.outside = outside
        self.inside = inside
        self.is_list_item = is_list_item
        self.legacy = legacy
        self.internal = internal
        self.box = box

    def is_none(self) -> bool:
        return self.box == DisplayBox.NONE

    def is_outside_and_inside(self) -> bool:
        return bool(self.outside and self.inside)

    def is_block(self) -> bool:
        return self.is_outside_and_inside() and self.outside == DisplayOutside.BLOCK

    def is_inline(self) -> bool:
        return self.is_outside_and_inside() and self.outside == DisplayOutside.INLINE

    def is_inline_block(self) -> bool:
        return (
            self.is_inline()
            and self.is_outside_and_inside()
            and self.inside == DisplayInside.FLOW_ROOT
        )

    @classmethod
    def create_inline(cls) -> Display:
        return Display(outside=DisplayOutside.INLINE, inside=DisplayInside.FLOW)

    def __str__(self):
        if self.box:
            return str(self.box)
        if self.internal:
            return str(self.internal)
        if self.legacy:
            return str(self.legacy)

        parts = []
        if self.outside:
            parts.append(str(self.outside))
        # Handle implicit inner/outer for serialization if needed, but for now just validation
        if self.inside:
            parts.append(str(self.inside))
        if self.is_list_item:
            parts.append("is_list_item=True")

        return " ".join(parts)

    def __repr__(self):
        return str(self)
