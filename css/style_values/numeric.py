from dataclasses import dataclass
from css.lexer import Num, Tok, Token
from .base import StyleValue

@dataclass
class IntegerValue(StyleValue):
    int_value: int

    def to_token(self) -> Token:
        return Token(type=Tok.NUMBER, val=self.int_value, num_type=Num.INTEGER)

    def __str__(self):
        return str(self.int_value)


@dataclass
class NumberValue(StyleValue):
    num_value: float

    def to_token(self) -> Token:
        return Token(type=Tok.NUMBER, val=self.num_value, num_type=Num.NUMBER)

    def __str__(self):
        return f"{self.num_value:g}"
