from dataclasses import dataclass
from css.property import Property
from .base import StyleValue
from css.lexer import Token


@dataclass
class ShorthandStyleValue(StyleValue):
    property: Property
    sub_properties: dict[Property, StyleValue]

    def to_token(self) -> Token:
        # Shorthand values are composed of multiple tokens, but we need to return a single token
        # This is a simplification - in practice, you might want to return a list or handle differently
        raise NotImplementedError(
            "ShorthandStyleValue.to_token() should not be called directly"
        )

    def __str__(self):
        return " ".join(str(v) for v in self.sub_properties.values())
