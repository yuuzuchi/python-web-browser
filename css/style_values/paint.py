from dataclasses import dataclass
from css.lexer import Tok, Token
from .base import StyleValue
from .color import ColorValue
from .url import URLValue
from .keyword import KeywordValue


@dataclass
class PaintValue(StyleValue):
    """
    The paint value can be:
    - A keyword: 'none', 'context-fill', or 'context-stroke'
    - A color value
    - A URL (typically referencing an SVG paint server like a gradient or pattern),
      optionally followed by a fallback of 'none' or a <color>
    """

    # can be a keyword ('none', 'context-fill', 'context-stroke'), a ColorValue, or a URLValue
    primary: KeywordValue | ColorValue | URLValue

    # fallback for URL values: can be 'none' keyword or a ColorValue
    # only used when primary is a URLValue
    fallback: KeywordValue | ColorValue | None = None

    def to_token(self) -> Token:
        return self.primary.to_token()

    def __str__(self):
        if self.fallback:
            return f"{self.primary} {self.fallback}"
        return str(self.primary)
