from dataclasses import dataclass
from css.lexer import Tok, Token
from .base import StyleValue


@dataclass
class ListStyleValue(StyleValue):
    items: list[StyleValue]
    delim: str

    # def to_token(self) -> list[Token]:
    #     out = []
    #     for i, item in enumerate(self.items):
    #         out.append(item.to_token())
    #         if i < len(self.items) - 1:
    #             out.append(Token(Tok.DELIM, self.delim))
    #             out.append(Token(Tok.WHITESPACE))
    #     return out

    def __str__(self):
        sep = self.delim
        if sep == " ":
            return f"[{" ".join(str(i) for i in self.items)}]"
        return f"[{f"{sep} ".join(repr(i) for i in self.items)}]"
