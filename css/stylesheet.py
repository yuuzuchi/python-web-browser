from __future__ import annotations
from url import URL
from css.style_rule import StyleRule
from dataclasses import dataclass
from css.enums import Origin

@dataclass
class CSSStylesheet:
    rules: list[StyleRule]
    origin: Origin
    absolute_url: URL

    def __str__(self):
        return "\n".join(map(str, self.rules))