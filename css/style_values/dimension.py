from css.units import LengthUnit
from typing import Any
from dataclasses import dataclass
import math
from css.lexer import Tok, Token
from .base import StyleValue


@dataclass
class DimensionValue(StyleValue):
    raw_value: float
    dim_unit: str

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)

    def __str__(self):
        return f"{self.raw_value:g}{self.dim_unit}"


@dataclass
class PercentageValue(DimensionValue):
    def __init__(self, raw_value: float):
        self.raw_value = raw_value
        self.dim_unit = "percent"

    @property
    def percentage(self):
        return self.raw_value

    def to_token(self) -> Token:
        return Token(type=Tok.PERCENTAGE, val=self.raw_value)

    def __str__(self):
        return f"{self.raw_value:g}%"


@dataclass
class AngleValue(DimensionValue):
    def __post_init__(self):
        assert self.dim_unit in ("deg", "grad", "rad", "turn")

    def to_degrees(self) -> float:
        if self.dim_unit == "grad":
            return self.raw_value / 400 * 360
        if self.dim_unit == "rad":
            return self.raw_value / math.pi * 360
        if self.dim_unit == "turn":
            return self.raw_value * 360
        return self.raw_value

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


@dataclass
class FlexValue(DimensionValue):
    def __init__(self, value):
        self.raw_value = value
        self.dim_unit = "fr"

    @property
    def flex(self):
        return self.raw_value


@dataclass
class Length:
    value: float
    unit: LengthUnit

    @classmethod
    def from_px(cls, px: float) -> "Length":
        return Length(px, unit=LengthUnit.PX)


@dataclass
class LengthValue(DimensionValue):
    def __init__(self, length: Length):
        self.length = length
        self.raw_value = length.value
        self.dim_unit = length.unit.value

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


@dataclass
class TimeValue(DimensionValue):
    def __post_init__(self):
        assert self.dim_unit.lower() in ("ms", "s")

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)
