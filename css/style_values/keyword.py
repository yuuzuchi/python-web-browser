from dataclasses import dataclass
from css.enums import Keyword
from css.lexer import Tok, Token
from .base import StyleValue


class KeywordValue(StyleValue):

    def __init__(self, keyword_str: str):
        self.keyword_str = keyword_str.lower()
        self.keyword = Keyword(self.keyword_str)

    @classmethod
    def from_keyword(cls, keyword: Keyword) -> "KeywordValue":
        """Create a KeywordValue from a Keyword enum."""
        instance = cls.__new__(cls)
        instance.keyword = keyword
        instance.keyword_str = keyword.value
        return instance

    def to_token(self) -> Token:
        return Token(type=Tok.IDENT, val=self.keyword.value)

    def __str__(self):
        return self.keyword_str

    def is_css_wide(self) -> bool:
        return self.keyword in (
            Keyword.INITIAL,
            Keyword.INHERIT,
            Keyword.UNSET,
            Keyword.REVERT,
            Keyword.REVERT_LAYER,
        )

    def is_color(self) -> bool:
        return self.keyword in (
            Keyword.ACCENTCOLOR,
            Keyword.ACCENTCOLORTEXT,
            Keyword.ACTIVETEXT,
            Keyword.BUTTONBORDER,
            Keyword.BUTTONFACE,
            Keyword.BUTTONTEXT,
            Keyword.CANVAS,
            Keyword.CANVASTEXT,
            Keyword.FIELD,
            Keyword.FIELDTEXT,
            Keyword.GRAYTEXT,
            Keyword.HIGHLIGHT,
            Keyword.HIGHLIGHTTEXT,
            Keyword.LINKTEXT,
            Keyword.MARK,
            Keyword.MARKTEXT,
            Keyword.SELECTEDITEM,
            Keyword.SELECTEDITEMTEXT,
            Keyword.VISITEDTEXT,
            Keyword.CURRENTCOLOR,
        )


@dataclass
class CSSWideKeywordValue(KeywordValue):
    def __post_init__(self):
        super().__post_init__()
        assert self.is_css_wide()
