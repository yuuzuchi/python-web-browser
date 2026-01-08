from __future__ import annotations
from css.lexer import Tok
from dataclasses import dataclass
from typing import Any

from css.lexer import Token


# ComponentValues from the spec
# Technically some Tokens are considered ComponentValues too
# https://www.w3.org/TR/css-syntax-3/#component-value


class ComponentValue:
    underlying: Token | Function | SimpleBlock

    def __init__(self, underlying: Token | Function | SimpleBlock | ComponentValue):
        # if passed a component value, unwrap it
        if isinstance(underlying, ComponentValue):
            self.underlying = underlying.underlying
        else:
            self.underlying = underlying

    @property
    def type(self) -> Tok:
        return self.underlying.type

    @property
    def val(self) -> Any:
        return self.underlying.val

    @property
    def token(self) -> Token:
        assert isinstance(self.underlying, Token)
        return self.underlying

    @property
    def tok_val(self) -> Any:
        assert isinstance(self.underlying, Token)
        return self.underlying.val

    def is_tok(self, type: Tok):
        return isinstance(self.underlying, Token) and self.underlying.type == type

    def is_block(self) -> bool:
        return isinstance(self.underlying, SimpleBlock)

    def is_function(self, name: str | None = None) -> bool:
        if not isinstance(self.underlying, Function):
            return False

        if name and self.underlying.name.val:
            return self.underlying.name.val.lower() == name.lower()

        return True

    def function(self) -> Function:
        assert isinstance(self.underlying, Function)
        return self.underlying

    def is_ident(self, val: str, case_insensitive=True) -> bool:
        if not isinstance(self.underlying, Token):
            return False

        if not self.underlying.val:
            return False

        return self.type == Tok.IDENT and (
            self.underlying.val.lower() == val.lower()
            if case_insensitive
            else self.underlying == val
        )

    def is_delim(self, delim: str) -> bool:
        if not isinstance(self.underlying, Token):
            return False

        if not self.underlying.val:
            return False

        return self.underlying.type == Tok.DELIM and self.underlying.val == delim

    def __repr__(self):
        return str(self.underlying)


@dataclass
class SimpleBlock:
    tok: Token
    val: list[Any]

    @property
    def type(self) -> Tok:
        return self.tok.type

    def __str__(self):
        mirror = self.tok.mirror()
        if not mirror:
            return f"({"".join(map(str, self.val))})"
        return f"{self.tok.val}{"".join(map(str, self.val))}{mirror.val}"


@dataclass
class Function:
    name: Token
    val: list[Any]

    @property
    def type(self) -> Tok:
        return self.name.type

    def __str__(self):
        return f"{self.name.val}({"".join(map(str, self.val))})"
