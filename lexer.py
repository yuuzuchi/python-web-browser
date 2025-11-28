from dataclasses import dataclass
from enum import Enum, auto

from history import HistoryManager

# https://www.w3.org/TR/css-syntax-3/#token-diagrams


class Tok(Enum):
    IDENT = auto()
    FUNCTION = auto()
    AT_KEYWORD = auto()
    HASH = auto()
    STRING = auto()
    BAD_STRING = auto()
    URL = auto()
    BAD_URL = auto()
    DELIM = auto()
    NUMBER = auto()
    PERCENTAGE = auto()
    DIMENSION = auto()
    WHITESPACE = auto()
    CDO = auto()
    CDC = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LBRAC = auto()
    RBRAC = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()


def matches_ident(c: str) -> bool:
    return c.isalnum or c in "_-" or not c.isascii()


def is_hex_digit(c: str) -> bool:
    return c.isdigit() or c in "abcdefABCDEF"


@dataclass
class Token:
    tok_type: Tok
    val: str


class Lexer:
    def __init__(self, s: str, history_manager: HistoryManager):
        self.s = s
        self.i = 0
        self.buffer = []
        self.history_manager = history_manager

    def expect(self, expected: Tok | str):
        tok = self.peek()
        if isinstance(expected, str):
            if tok.val == expected:
                return self.next()
            else:
                raise SyntaxError(f"Expected literal {expected}, got {tok.value}")
        else:
            if tok.tok_type == expected:
                return self.next()
            else:
                SyntaxError(f"Expected token {expected}, got {tok.tok_type}")

    def _produce_token(self) -> Token:
        self.whitespace()
        c = self.next_char()

        if c == "/" and self.peek_char() == "*":
            self.comment()

        if matches_ident(c):
            return self.lex_ident()

        if c.isdigit() or c in "+-.":
            return self.lex_number()

        if self.peek().tok_type == Tok.IDENT and self.peek().val == "url":
            return self.lex_url()

    def next_char(self) -> str:
        if self.i < len(self.s):
            self.i += 1
            return self.s[self.i - 1]
        return None

    def peek_char(self, steps=1) -> str:
        if self.i + steps < len(self.s):
            return self.s[self.i + steps]

    def peek(self, k=1) -> Token:
        while len(self.buffer) < k:
            tok = self._produce_token()
            self.buffer.append(tok)
        return self.buffer[k - 1]

    def next(self) -> Token:
        if self.buffer:
            return self.buffer.pop(0)
        return self._produce_token()

    def whitespace(self) -> None:
        while self.peek_char().isspace():
            self.next_char()

    def comment(self) -> None:
        c = self.next_char()
        while not (c == "*" and self.peek_char() == "/"):
            c = self.next_char()

    def consume_escape(self) -> str:
        self.next_char()
        c = self.next_char()
        if c is None:
            return "\\"
        if is_hex_digit(c):
            digits = []
            if is_hex_digit(self.peek_char()) and len(digits) < 6:
                digits.append(self.next_char())
            if self.peek_char().isspace():
                self.next_char()
            return "".join(digits)
        return self.next_char()

    def lex_ident(self) -> Token:
        s = [self.next_char()]
        while True:
            c = self.peek_char()
            if matches_ident(c):
                s.append(self.next_char())
            elif c == "\\":
                s.append(self.consume_escape())
            else:
                break
        return Token(Tok.IDENT, "".join(s))

    def lex_token(self) -> Token:
        pass

    def lex_at_keyword(self) -> Token:
        pass

    def lex_hash(self) -> Token:
        pass

    def lex_string(self) -> Token:
        pass

    def lex_url(self) -> Token:
        pass

    def lex_number(self) -> Token:
        s = [self.next_char()]
        num_dots = 0
        while True:
            c = self.peek_char()
            if c.isdigit():
                s.append(self.next_char())
            elif c == ".":
                num_dots += 1
                if num_dots > 1:
                    break
                s.append(self.next_char())
            else:
                break

        if self.peek_char().lower() == "e":
            s.append(self.next_char())
            if self.peek_char() in "+-":
                s.append(self.next_char())
            while self.peek_char().isdigit():
                s.append(self.next_char())

        return "".join(s)
