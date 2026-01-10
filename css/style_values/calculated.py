from dataclasses import dataclass
from .base import StyleValue

@dataclass
class CalculatedValue(StyleValue):
    # TODO: Implement proper calculation value handling
    def to_token(self):
        raise NotImplementedError("CalculatedValue.to_token() not yet implemented")
