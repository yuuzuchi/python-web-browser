from dataclasses import dataclass, field
from typing import Any, Optional

from lexer import Token


# ComponentValues from the spec
# Technically some Tokens are considered ComponentValues too
class Component:
    pass


@dataclass
class SimpleBlock(Component):
    tok: Token
    val: list[Any]

    @property
    def type(self):
        return self.tok.type


@dataclass
class Function(Component):
    name: Token
    val: list[Any]

    @property
    def type(self):
        return self.name.type


@dataclass
class Rule:
    prelude: list
    block: Optional[Any]
    location: Optional[Any] = None


@dataclass
class AtRule(Rule):
    name: str = ""


@dataclass
class QualifiedRule(Rule):
    block: list[Any] = field(default_factory=list)

    @property
    def selectors(self):
        return self.prelude


@dataclass
class Stylesheet:
    location: Optional[str]
    val: list[Rule]


@dataclass
class Declaration:
    name: str
    val: list[Token]
    important: bool = False