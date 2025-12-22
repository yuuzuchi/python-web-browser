from dataclasses import dataclass
from typing import Any

from css.lexer import Token


# ComponentValues from the spec
# Technically some Tokens are considered ComponentValues too
# https://www.w3.org/TR/css-syntax-3/#component-value

class Component:
    pass


@dataclass
class SimpleBlock(Component):
    tok: Token
    val: list[Any]

    @property
    def type(self):
        return self.tok.type

    def __str__(self):
        return f"{self.tok.val}{"".join(map(str, self.val))}{self.tok.mirror().val}"


@dataclass
class Function(Component):
    name: Token
    val: list[Any]

    @property
    def type(self):
        return self.name.type

    def __str__(self):
        return f"{self.name.val}({"".join(map(str, self.val))})"
