from dataclasses import dataclass
from .base import StyleValue


class BasicShape:
    pass


@dataclass
class BasicShapeValue(StyleValue):
    basic_shape: BasicShape
