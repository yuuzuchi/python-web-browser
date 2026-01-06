from __future__ import annotations
from log import warn

from css.enums import Property

from dataclasses import field
from css.units import LengthUnit
from typing import Any
from dataclasses import dataclass
import math
from typing import TYPE_CHECKING
from css.lexer import Tok, Token
from .base import StyleValue

# resolve circular import
if TYPE_CHECKING:
    from css.compute_context import ComputeContext
    from dom import Node


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
        return self.raw_value / 100

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
class FontMetrics:
    font_size: float
    line_height: float


@dataclass
class LengthResolutionContext:
    vw: int
    vh: int
    font_metrics: FontMetrics
    root_font_metrics: FontMetrics

    @classmethod
    def for_element(cls, node: Node, vw: int, vh: int) -> "LengthResolutionContext":
        style = node.computed_style
        root_style = node.get_root().computed_style
        """Returns a LengthResolutionContext object for a given **computed** node.
        *TODO:* access information about viewport from each node. Requires passed vw and vh for now.
        """
        font_metrics = FontMetrics(
            font_size=style.computed_font_size(),
            line_height=style.computed_line_height(),
        )
        root_font_metrics = FontMetrics(
            font_size=root_style.computed_font_size(),
            line_height=root_style.computed_line_height(),
        )
        return LengthResolutionContext(
            vw=vw, vh=vh, font_metrics=font_metrics, root_font_metrics=root_font_metrics
        )


@dataclass
class Length:
    value: float
    unit: LengthUnit

    @classmethod
    def from_px(cls, px: float) -> "Length":
        return Length(px, unit=LengthUnit.PX)

    def to_px(self) -> "Length":
        if self.unit == LengthUnit.IN:
            return Length(self.value * 96, unit=LengthUnit.PX)
        if self.unit == LengthUnit.CM:
            return Length(self.value * 37.8, unit=LengthUnit.PX)
        if self.unit == LengthUnit.MM:
            return Length(self.value * 3.78, unit=LengthUnit.PX)
        if self.unit == LengthUnit.PT:
            return Length(self.value * 4 / 3, unit=LengthUnit.PX)
        if self.unit == LengthUnit.PC:
            return Length(self.value * 16, unit=LengthUnit.PX)
        if self.unit == LengthUnit.Q:
            return Length(self.value * 0.944, unit=LengthUnit.PX)
        return self  # px value


@dataclass
class LengthValue(DimensionValue):
    def __init__(self, length: Length):
        self.length = length
        self.raw_value = length.value
        self.dim_unit = length.unit.value

    def absolutize(self, context: ComputeContext) -> LengthValue:
        res = context.length_context
        unit = self.length.unit
        val = self.length.value

        if unit == LengthUnit.PX:
            return self

        # context-relative units
        if unit == LengthUnit.EM:
            return LengthValue(Length.from_px(val * res.font_metrics.font_size))
        if unit == LengthUnit.REM:
            return LengthValue(Length.from_px(val * res.root_font_metrics.font_size))
        if unit == LengthUnit.VW or unit == LengthUnit.VI:
            # TODO: support writing directions
            return LengthValue(Length.from_px(val * res.vw / 100))
        if unit == LengthUnit.VH or unit == LengthUnit.VB:
            return LengthValue(Length.from_px(val * res.vh / 100))
        if unit == LengthUnit.VMIN:
            return LengthValue(Length.from_px(val * min(res.vw, res.vh) / 100))
        if unit == LengthUnit.VMAX:
            return LengthValue(Length.from_px(val * max(res.vw, res.vh) / 100))
        if unit == LengthUnit.LH:
            return LengthValue(Length.from_px(val * res.font_metrics.line_height))
        if unit == LengthUnit.RLH:
            return LengthValue(Length.from_px(val * res.root_font_metrics.line_height))

        # other absolute physical units (cm, mm, in, pt, pc, q)
        px_length = self.length.to_px()
        if px_length.unit == LengthUnit.PX:
            return LengthValue(px_length)

        warn(f"Cannot absolutize length value, unrecognized unit {unit}")
        return self

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


@dataclass
class TimeValue(DimensionValue):
    def __post_init__(self):
        assert self.dim_unit.lower() in ("ms", "s")

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)
