from dataclasses import field
from css.selectors import Selector
from css.enums import Origin
from dataclasses import dataclass
from css.style_declaration import StyleDeclaration


@dataclass(eq=False)
class StyleRule:
    selector_list: list[Selector]
    declarations: list[StyleDeclaration]
    source_order: int
    origin: Origin
    is_style_attribute: bool = False
    specificity: tuple[int, int, int] = field(init=False)
    _sort_key: tuple[Origin, bool, int, int, int, int] = field(init=False)

    def __post_init__(self):
        self.specificity = (0, 0, 0)
        if self.selector_list:
            self.specificity = max(s.specificity for s in self.selector_list)

        self._sort_key = (
            self.origin,
            self.is_style_attribute,
            *self.specificity,
            self.source_order,
        )  # type: ignore

    def get_sort_key(self, important: bool) -> tuple[int, bool, int, int, int, int]:
        origin = self.origin
        if important and 0 <= self.origin.value <= 2:
            origin = Origin(6 - self.origin.value)
        elif not important and 4 <= self.origin.value <= 6:
            origin = Origin(6 - self.origin.value)

        _, a, b, c, d, e = self._sort_key
        return origin.value, a, b, c, d, e

    def __str__(self) -> str:
        res = f"/* origin={self.origin.name} specificity={self.specificity} source_order={self.source_order} */\n"
        selectors = ", ".join(str(s) for s in self.selector_list)
        res += f"{selectors} {{\n"
        for decl in self.declarations:
            # Add indentation
            decl_lines = str(decl).split("\n")
            for line in decl_lines:
                res += f"  {line}\n"

        res += "}"
        return res
