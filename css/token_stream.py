from css.components import ComponentValue
from css.lexer import Tok, Token
from typing import Sequence
from log import log

class CSSTokenStream:

    def __init__(self, tokens: Sequence[Token | ComponentValue]):
        self.cursor: int = 0
        self.tokens = tokens
        self.cur = None
        self.marks: list[int] = []
        self.committed = False
        self.snapshot = [self.cursor, self.marks[:]]

    # ONLY TO BE USED IN CSS PARSER
    def next(self) -> Token | ComponentValue:
        self.cursor += 1
        if self.cursor > len(self.tokens):
            return Token(type=Tok.EOF, val=None)

        res = self.tokens[self.cursor - 1]
        return res

    def peek(self, n: int = 1) -> ComponentValue:
        if 0 <= self.cursor + n - 1 < len(self.tokens):
            return ComponentValue(self.tokens[self.cursor + n - 1])
        else:
            return ComponentValue(Token(type=Tok.EOF, val=None))

    def has_next(self) -> bool:
        return (
            self.cursor < len(self.tokens) and self.tokens[self.cursor].type != Tok.EOF
        )

    def consume(self) -> ComponentValue:
        self.cur = self.tokens[self.cursor]
        self.next()
        return ComponentValue(self.cur)

    def accept(self, type: Tok | None, val=None) -> ComponentValue | bool:
        n = self.peek()
        if not isinstance(n.underlying, Token):
            return False
        if type and not n.is_tok(type):
            return False
        if val and n.tok_val != val:
            return False
        return self.consume()

    def mark(self) -> None:
        self.marks.append(self.cursor)

    def restore_mark(self) -> None:
        self.cursor = self.marks.pop()

    def consume_whitespace(self) -> Token | None:
        is_whitespace = False
        while self.peek().is_tok(Tok.WHITESPACE):
            is_whitespace = True
            self.consume()

        return Token(type=Tok.WHITESPACE, val=None) if is_whitespace else None

    def consume_until(self, type: Tok, val=None) -> None:
        while True:
            n = self.peek()
            if n.is_tok(type):
                if n.tok_val == val or not val:
                    return
            if n.is_tok(Tok.EOF):
                return
            self.consume()

    def reset(self) -> None:
        self.cursor = 0

    def is_only_whitespace(self) -> bool:
        return all(tok.type == Tok.WHITESPACE for tok in self.tokens)

    # transactions: revert token stream state if transaction isn't committed.
    # with stream.transaction() as tx:
    #    tx.commit()
    # if the block is exited before the commit, a rollback will occur.
    class _Transaction:
        def __init__(self, stream: "CSSTokenStream"):
            self.stream = stream
            self.cursor_snap, self.marks_snap = stream.cursor, stream.marks[:]
            self.committed = False

        def commit(self) -> None:
            self.committed = True

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            if not self.committed:
                self.stream.cursor = self.cursor_snap
                self.stream.marks = self.marks_snap

    def transaction(self):
        return self._Transaction(self)

if __name__ == "__main__":
    ts = CSSTokenStream(
        [Token(Tok.IDENT, "1"), Token(Tok.IDENT, "2"), Token(Tok.IDENT, "3")]
    )
    with ts.transaction() as tx:
        print("First next() call:", ts.next())

        # if the context is exited before .commit(), stream will be restored
        demo_error = True
        if not demo_error:
            tx.commit()
    print("Second next() call:", ts.next())
