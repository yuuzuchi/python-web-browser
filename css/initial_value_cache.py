from log import warn
from ast import Assert
from css.enums import Property
from css.parser import Declaration
from css.property import PROPERTIES
from css.style_values.base import StyleValue


_initial_value_cache = {}

# TODO: replace warns with asserts after value parser is completed
def property_initial_value(property: Property) -> StyleValue:
    """Gets initial values for given property, and caches the result."""
    # initial value for property cache hit
    if property in _initial_value_cache:
        return _initial_value_cache[property]

    # get initial values (str) from css_property.py
    property_as_string = property.value
    initial_value_as_string = PROPERTIES.get(property_as_string, {}).get("initial")

    # Property has no initial value
    if not initial_value_as_string:
        warn(f"No initial value for property {property}")
        return

    # tokenize as a css value
    # FIXME: there is no CSSSyntaxParser.parse_css_value(),
    # I'm currently just piggybacking off of parse_declaration
    from css.parser import CSSSyntaxParser

    decl = CSSSyntaxParser().parse_declaration(
        f"{property_as_string}: {initial_value_as_string}"
    )

    assert isinstance(decl, Declaration)
    from css.property_parser import PropertyParser

    if out := PropertyParser(decl.val).parse_entire_value(property):
        _initial_value_cache[property] = out
        return out

    warn(f"Could not parse intial value for property {property}")
