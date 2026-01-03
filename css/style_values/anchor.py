from dataclasses import dataclass
from css.enums import AnchorSize
from .base import StyleValue
from .dimension import DimensionValue, LengthValue, PercentageValue
from .keyword import KeywordValue


@dataclass
class AnchorSizeValue(StyleValue):
    anchor_name: str | None
    anchor_side: AnchorSize | None
    fallback: DimensionValue | None


@dataclass
class AnchorValue(StyleValue):
    anchor_name: str | None
    anchor_side: PercentageValue | KeywordValue | AnchorSizeValue
    fallback: LengthValue | PercentageValue | AnchorSizeValue | None
