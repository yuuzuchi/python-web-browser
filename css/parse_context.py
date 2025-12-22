from dataclasses import dataclass
from css.enums import Origin


@dataclass
class ParseContext:
    origin: Origin
    source_order: int = 0
