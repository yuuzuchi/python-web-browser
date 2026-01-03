from dataclasses import dataclass
from url import URL
from css.lexer import Tok, Token
from .base import StyleValue

@dataclass
class URLValue(StyleValue):
    url_str: str
    url: URL | None = None
    # parser may initially pass only url_str; url can be resolved later with base URL context

    def to_token(self) -> Token:
        return Token(type=Tok.URL, val=self.url_str)

    def __str__(self):
        return f"url('{self.url_str}')"
