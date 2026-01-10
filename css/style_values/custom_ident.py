from dataclasses import dataclass
from css.style_values.base import StyleValue


@dataclass
class CustomIdentValue(StyleValue):
    ident: str

    def __post_init__(self):
        assert self.ident not in (
            "inherit",
            "initial",
            "unset",
            "revert",
            "revert-layer",
            "default",
        )

    def is_dashed(self) -> bool:
        return self.ident.startswith("--")
