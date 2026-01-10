from dataclasses import dataclass
from css.lexer import Tok, Token
from .base import StyleValue

@dataclass
class StringValue(StyleValue):
    string: str

    def to_token(self) -> Token:
        return Token(type=Tok.STRING, val=self.string)

    def __str__(self):
        return f"'{self.string}'"
