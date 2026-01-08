from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from css.compute_context import ComputeContext
    from css.lexer import Token

class StyleValue:

    def absolutize(self, context: ComputeContext):
        """Compute a value. Requires a ComputeContext, required for absolutizing LengthValues."""
        # overriden by children. Most stylevalues are already absolutized, simply return self.
        return self

    def to_token(self) -> Token:
        raise AssertionError("Cannot serialize generic StyleValue")

    def __str__(self):
        return repr(self)
