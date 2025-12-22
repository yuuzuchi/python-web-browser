from css.lexer import Token

class StyleValue:
    def to_token(self) -> Token:
        pass

    def __str__(self):
        return repr(self)
