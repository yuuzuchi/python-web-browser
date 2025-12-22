from dataclasses import dataclass
from url import URL
from css.lexer import Tok, Token
from .base import StyleValue

@dataclass
class URLValue(StyleValue):
    url_str: str
    url: URL
    # parser is responsible for passing both the original value and the resolveed URL object

    def to_token(self) -> Token:
        return Token(type=Tok.URL, val=self.url_str)

    def __str__(self):
        return f"url('{self.url_str}')"
