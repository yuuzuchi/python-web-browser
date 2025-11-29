from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Generator, Optional

from history import HistoryManager


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
    EOF = auto()


class Hash(Enum):
    ID = "id"
    UNRESTRICTED = "unrestricted"


class Num(Enum):
    INTEGER = "int"
    NUMBER = "number"


def is_ident_start(c: str) -> bool:
    if c == None:
        return False
    return c in "_" or c.isalpha() or not c.isascii()


def is_ident(c: str) -> bool:
    if c == None:
        return False
    return is_ident_start(c) or c == "-" or c.isdigit()


def is_hex_digit(c: str) -> bool:
    return c.isdigit() or c in "abcdefABCDEF"


@dataclass
class Token:
    tok_type: Tok
    val: Optional[Any] = ""
    hash_type: Optional[Hash] = Hash.UNRESTRICTED
    num_type: Optional[Num] = Num.INTEGER
    dim_unit: Optional[str] = ""

    def __repr__(self):
        return f"<tok.{self.tok_type.name} val='{self.val}'>"


class Lexer:
    def __init__(self, s: str, history_manager: HistoryManager):
        self.s = s
        self.i = 0
        self.history_manager = history_manager

    def parse(self) -> Generator[Token]:
        while True:
            tok = self.consume()
            yield tok
            if tok.tok_type == Tok.EOF:
                return

    def next_char(self) -> str:
        if self.i < len(self.s):
            self.i += 1
            return self.s[self.i - 1]
        return None

    def peek(self, n, length=1) -> str:
        if 0 < self.i + n < len(self.s):
            return self.s[self.i + n : self.i + n + length]

    def parse_error(self):
        print(
            f"Parse Error at idx {self.i}:\n{self.s[self.i-15:self.i]}>>>{self.s[self.i]}<<<{self.s[self.i+1:self.i+15]}"
        )

    # https://www.w3.org/TR/css-syntax-3/#consume-token
    def consume(self) -> Token:
        self.consume_comment()
        c = self.next_char()

        if c == None:
            return Token(Tok.EOF)

        if c.isspace():
            return self.consume_whitespace()

        if c == '"':
            return self.consume_string('"')

        if c == "#":
            if is_ident(self.peek(0)) or self.is_valid_escape(offset=1):
                hash_tok = Token(Tok.HASH, self.consume_ident())
                if self.next_3_starts_ident():
                    hash_tok.hash_type = Hash.ID
                return hash_tok
            return Token(Tok.DELIM, c)

        if c == "'":
            return self.consume_string("'")

        if c == "(":
            return Token(Tok.LPAREN)

        if c == ")":
            return Token(Tok.RPAREN)

        if c == "+":
            if c.isdigit():
                self.reconsume()
                return self.consume_numeric()
            return Token(Tok.DELIM, c)

        if c == ",":
            return Token(Tok.COMMA)

        if c == "-":
            if self.next_3_starts_number():
                self.reconsume()
                return self.consume_numeric()
            if self.peek(0, length=2) == "->":
                self.next_char()
                self.next_char()
                return Token(Tok.CDC)
            if is_ident_start(self.peek(0)):
                self.reconsume()
                return self.consume_ident()
            return Token(Tok.DELIM, c)

        if c == ":":
            return Token(Tok.COLON)

        if c == ";":
            return Token(Tok.SEMICOLON)

        if c == "<":
            if self.peek(0, length=3) == "!--":
                self.next_char()
                self.next_char()
                self.next_char()
                return Token(Tok.CDO)
            return Token(Tok.DELIM, c)

        if c == "@":
            if self.next_3_starts_ident():
                return Token(Tok.AT_KEYWORD, self.consume_ident_seq())
            return Token(Tok.DELIM, c)

        if c == "[":
            return Token(Tok.LBRAC)

        if c == "\\":
            if self.is_valid_escape():
                self.reconsume()
                return self.consume_ident()
            self.parse_error()
            return Token(Tok.DELIM, c)

        if c == "]":
            return Token(Tok.RBRAC)

        if c == "{":
            return Token(Tok.LBRACE)

        if c == "}":
            return Token(Tok.RBRACE)

        if c.isdigit():
            self.reconsume()
            return self.consume_numeric()

        if is_ident_start(c):
            self.reconsume()
            return self.consume_ident()

        return Token(Tok.DELIM, c)

    def consume_whitespace(self) -> Token:
        while self.peek(0) != None and self.peek(0).isspace():
            self.next_char()
        return Token(Tok.WHITESPACE)

    def consume_string(self, ending_quote: str) -> Token:
        res = []
        while True:
            c = self.next_char()
            if c == ending_quote:
                return Token(Tok.STRING, "".join(res))
            if c == None:
                self.parse_error()
                return Token(Tok.STRING, "".join(res))
            if c == "\n":
                self.parse_error()
                self.reconsume()
                return Token(Tok.BAD_STRING)
            if c == "\\":
                if not self.peek(0):
                    continue
                if self.peek(0) == "\n":
                    self.next_char()
                else:
                    res.append(self.consume_escape())
            else:
                res.append(c)

    def consume_comment(self) -> None:
        if self.peek(0, length=2) == "/*":
            while self.peek(0, length=2) not in ["*/", None]:
                self.next_char()
            if self.peek(0) == None:
                self.parse_error()

    def is_valid_escape(self, offset=0) -> bool:
        if self.peek(-1 + offset) != "\\" or self.peek(offset) == "\n":
            return False
        return True

    def next_3_starts_ident(self) -> bool:
        c = self.peek(0)
        if c == "-":
            c2 = self.peek(1)
            return is_ident_start(c2) or c2 == "-" or self.is_valid_escape(offset=2)
        if is_ident_start(c):
            return True
        if c == "\\":
            return self.is_valid_escape(offset=1)
        return False

    def next_3_starts_number(self, offset=0) -> bool:
        c = self.peek(offset)
        c2 = self.peek(1 + offset)
        if c in ["+", "-"]:
            if c2.isdigit():
                return True
            return c2 == "." and self.peek(2 + offset).isdigit()
        if c == ".":
            return c2.isdigit()
        return c.isdigit()

    def reconsume(self) -> None:
        if self.i > 0:
            self.i -= 1

    def consume_ident_seq(self) -> str:
        res = []
        c = self.next_char()
        while True:
            if is_ident(c):
                res.append(c)
            elif self.is_valid_escape():
                res.append(self.consume_escape())
            else:
                if c != None:
                    self.reconsume()
                return "".join(res)
            c = self.next_char()

    def consume_ident(self) -> Token:
        string = self.consume_ident_seq()
        if string.lower() == "url" and self.peek(1) == "(":
            self.next_char()
            while self.peek(0, length=2).isspace():
                self.next_char()
            c1, c2 = self.peek(0), self.peek(1)
            if c1 in "\"'" or (c1.isspace() and c2 in "\"'"):
                return Token(Tok.FUNCTION, string)
            return self.consume_url()
        elif self.peek(0) == "(":
            self.next_char()
            return Token(Tok.FUNCTION, string)
        return Token(Tok.IDENT, string)

    def consume_url(self) -> Token:
        url_tok = Token(Tok.URL, "")
        self.consume_whitespace()
        while True:
            c = self.next_char()
            if c == ")":
                return url_tok
            if c == None:
                self.parse_error()
                return url_tok
            if c.isspace():
                self.consume_whitespace()
                if self.peek(1) in [None, ")"]:
                    if self.peek(1) == None:
                        self.parse_error()
                    self.next_char()
                    return url_tok
                else:
                    self.consume_bad_url_remnants()
                    return Token(Tok.BAD_URL)
            if c in "\"'(":
                self.consume_bad_url_remnants()
                return Token(Tok.BAD_URL)

            if c == "\\":
                if self.is_valid_escape():
                    url_tok.val += self.consume_escape()
                else:
                    self.parse_error()
                    self.consume_bad_url_remnants()
                    return Token(Tok.BAD_URL)
            else:
                url_tok.val += c

    def consume_bad_url_remnants(self) -> None:
        while True:
            c = self.next_char()
            if c == ")" or c == None:
                return
            if self.is_valid_escape():
                self.consume_escape()

    def consume_numeric(self) -> Token:
        num, t = self.consume_number()
        if self.next_3_starts_ident():
            dimension_tok = Token(Tok.DIMENSION, num, num_type=t, dim_unit="")
            dimension_tok.unit = self.consume_ident_seq()
            return dimension_tok
        elif self.peek(0) == "%":
            self.next_char()
            return Token(Tok.PERCENTAGE, num)
        return Token(Tok.NUMBER, num, num_type=t)

    def consume_number(self) -> tuple[str, Num]:
        t = Num.INTEGER
        res = []
        if self.peek(0) in "+-":
            res.append(self.next_char())
        while self.peek(0).isdigit():
            res.append(self.next_char())
        if self.peek(0) == "." and self.peek(1).isdigit():
            res.append(self.next_char())
            res.append(self.next_char())
            t = Num.NUMBER
            while self.peek(0).isdigit():
                res.append(self.next_char())
        if self.peek(0).lower() == "e":
            consume_len = 0
            if self.peek(1).isdigit():
                consume_len = 2
            elif self.peek(1) in "+-" and self.peek(2).isdigit():
                consume_len = 3

            if consume_len:
                for _ in range(consume_len):
                    res.append(self.next_char())
                t = Num.NUMBER
                while self.peek(0).isdigit():
                    res.append(self.next_char())

        return self.string_to_number("".join(res)), t

    def consume_escape(self) -> str:
        c = self.next_char()
        if is_hex_digit(c):
            # return code point associated with hex value, e.g. \FFFD -> REPLACEMENT_CHARACTER(�)
            hex_num = [c]
            while is_hex_digit(self.peek(0)) and len(hex_num) < 6:
                hex_num.append(self.next_char())

            if self.peek(0).isspace():
                self.consume_whitespace()

            hex_num = int("".join(hex_num), 16)
            if not hex_num:
                return chr(0)
            if 0xD800 <= hex_num <= 0xDFFF or hex_num > 0x10FFFF:
                return chr(0xDFFF)
            return chr(hex_num)
        if c == None:
            self.parse_error()
            return chr(0xDFFF)

        return c

    def string_to_number(self, s) -> int:
        n = len(s)
        i = 0

        # sign
        sign = 1
        if i < n and s[i] in "+-":
            if s[i] == "-":
                sign = -1
            i += 1

        # integer part
        int_start = i
        while i < n and s[i].isdigit():
            i += 1
        int_part = int(s[int_start:i] or "0")

        # fractional part
        frac_part = 0
        frac_len = 0
        if i < n and s[i] == ".":
            i += 1
            frac_start = i
            while i < n and s[i].isdigit():
                i += 1
            frac_str = s[frac_start:i]
            if frac_str:
                frac_part = int(frac_str)
                frac_len = len(frac_str)

        # exponent
        exp = 0
        exp_sign = 1
        if i < n and s[i] in "eE":
            i += 1
            if i < n and s[i] in "+-":
                if s[i] == "-":
                    exp_sign = -1
                i += 1
            exp_start = i
            while i < n and s[i].isdigit():
                i += 1
            exp_str = s[exp_start:i]
            if exp_str:
                exp = int(exp_str)

        # value
        return (
            sign * (int_part + frac_part * 10 ** (-frac_len)) * 10 ** (exp_sign * exp)
        )


if __name__ == "__main__":
    with open("browser.css", "r") as f:
        lexer = Lexer(f.read(), HistoryManager())

        for token in lexer.parse():
            print(token)
