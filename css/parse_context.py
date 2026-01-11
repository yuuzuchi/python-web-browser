from url import URL
from dataclasses import dataclass
from css.enums import Origin


@dataclass
class ParseContext:
    origin: Origin
    absolute_url: URL
    source_order: int = 0
