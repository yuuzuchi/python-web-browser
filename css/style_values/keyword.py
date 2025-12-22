from dataclasses import dataclass
from css.enums import Keyword
from css.lexer import Tok, Token
from .base import StyleValue


@dataclass
class KeywordValue(StyleValue):
    keyword_str: str

    def __post_init__(self):
        self.keyword = Keyword(self.keyword_str)

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
