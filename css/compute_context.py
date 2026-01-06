from dataclasses import dataclass
from css.style_values.dimension import LengthResolutionContext

@dataclass
class ComputeContext:
    length_context: LengthResolutionContext
