from css.style_values.dimension import Percentage
from css.style_values.dimension import Length
from dataclasses import dataclass
from css.lexer import Tok, Token
from .base import StyleValue


@dataclass
class FitContentValue(StyleValue):
    length_percentage: Length | Percentage | None = None

    def to_token(self) -> Token:
        if isinstance(self.length_percentage, Length):
            return Token(
                type=Tok.DIMENSION,
                val=self.length_percentage.value,
                dim_unit=str(self.length_percentage.unit),
            )
        elif isinstance(self.length_percentage, Percentage):
            return Token(type=Tok.PERCENTAGE, val=self.length_percentage.value)
        else:
            return Token(type=Tok.IDENT, val="fit-content")

    def __str__(self):
        return str(self.length_percentage)
