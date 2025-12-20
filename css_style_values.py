from dataclasses import dataclass, field
import math
from typing import Optional
from enums import Keyword
from css_property import Property
from url import URL

from lexer import Num, Tok, Token


class StyleValue:
    def to_token(self) -> Token:
        pass


@dataclass
class KeywordValue(StyleValue):
    keyword_str: str
    keyword: Optional[Keyword] = None

    def __post_init__(self):
        if not self.keyword:
            self.keyword = Keyword.from_string(self.keyword_str)

    def to_token(self) -> Token:
        return Token(type=Tok.IDENT, val=self.keyword.value)

    def is_css_wide(self) -> bool:
        return self.keyword in (Keyword.INITIAL, Keyword.INHERIT, Keyword.UNSET, Keyword.REVERT, Keyword.REVERT_LAYER)


@dataclass
class CSSWideKeywordValue(KeywordValue):
    def __post_init__(self):
        assert self.is_css_wide()


@dataclass
class CustomIdentValue(KeywordValue):
    def __post_init__(self):
        assert not self.is_css_wide() and self.keyword != Keyword.DEFAULT


@dataclass
class StringValue(StyleValue):
    string: str

    def to_token(self) -> Token:
        return Token(type=Tok.STRING, val=self.string)


@dataclass
class URLValue(StyleValue):
    url_str: str
    url: URL
    # parser is responsible for passing both the original value and the resolveed URL object

    def to_token(self) -> Token:
        return Token(type=Tok.URL, val=self.url_str)


@dataclass
class IntegerValue(StyleValue):
    int_value: int

    def to_token(self) -> Token:
        return Token(type=Tok.NUMBER, val=self.int_value, num_type=Num.INTEGER)


@dataclass
class NumberValue(StyleValue):
    num_value: float

    def to_token(self) -> Token:
        return Token(type=Tok.NUMBER, val=self.num_value, num_type=Num.NUMBER)


@dataclass
class CalculatedValue(StyleValue):
    pass


@dataclass
class DimensionValue(StyleValue):
    raw_value: float
    dim_unit: str

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


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
class LengthValue(DimensionValue):
    def __post_init__(self):
        LENGTH_UNITS = [
            "Cap",
            "Ch",
            "Cm",
            "Dvb",
            "Dvh",
            "Dvi",
            "Dvmax",
            "Dvmin",
            "Dvw",
            "Em",
            "Ex",
            "Ic",
            "In",
            "Lh",
            "Lvb",
            "Lvh",
            "Lvi",
            "Lvmax",
            "Lvmin",
            "Lvw",
            "Mm",
            "Pc",
            "Pt",
            "Px",
            "Q",
            "Rcap",
            "Rch",
            "Rem",
            "Rex",
            "Ric",
            "Rlh",
            "Svb",
            "Svh",
            "Svi",
            "Svmax",
            "Svmin",
            "Svw",
            "Vb",
            "Vh",
            "Vi",
            "Vmax",
            "Vmin",
            "Vw",
        ]
        assert self.dim_unit.lower() in LENGTH_UNITS

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


@dataclass
class TimeValue(DimensionValue):
    def __post_init__(self):
        assert self.dim_unit.lower() in ("ms", "s")

    def to_token(self) -> Token:
        return Token(type=Tok.DIMENSION, val=self.raw_value, dim_unit=self.dim_unit)


@dataclass
class ShorthandStyleValue(StyleValue):
    property: Property
    sub_properties: dict[Property:StyleValue]


@dataclass
class ListStyleValue(StyleValue):
    items: list[StyleValue]
    delim: str

    def to_token(self) -> list[Token]:
        out = []
        for i, item in self.items:
            out.append(item.to_token())
            if i < len(self.items) - 1:
                out.append(Token(Tok.DELIM, self.delim))
                out.append(Token(Tok.WHITESPACE))
        return out
