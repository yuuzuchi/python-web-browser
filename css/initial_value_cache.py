from ast import Assert
from css.enums import Property
from css.parser import Declaration
from css.property import PROPERTIES
from css.style_values.base import StyleValue


_initial_value_cache = {}


def property_initial_value(property: Property) -> StyleValue:
    # initial value for property cache hit
    if property in _initial_value_cache:
        return _initial_value_cache[property]

    # get initial values (str) from css_property.py
    property_as_string = property.value
    initial_value_as_string = PROPERTIES.get(property_as_string, {}).get("initial")

    assert initial_value_as_string

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

    raise AssertionError("fCould not parse intial value for property {property}")
