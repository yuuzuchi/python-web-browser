from __future__ import annotations
from css.style_rule import StyleRule
from dataclasses import dataclass
from css.enums import Origin

@dataclass
class CSSStylesheet:
    rules: list[StyleRule]
    origin: Origin

    def __str__(self):
        return "\n".join(map(str, self.rules))