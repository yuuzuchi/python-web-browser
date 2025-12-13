# https://www.w3.org/TR/css-syntax-3/#parse-grammar
import collections
from typing import Any, Generator, Optional
from history import HistoryManager
from html_parser import Element, Text
from dataclasses import dataclass, field

from lexer import Lexer, Tok, Token
from selectors_new import (
    AttributeMatch,
    AttributeSelector,
    Selector,
    ClassSelector,
    Combinator,
    ComplexSelector,
    CompoundSelector,
    IDSelector,
    PseudoClassSelector,
    PseudoElement,
    SimpleSelector,
    TypeSelector,
    UniversalSelector,
)

DEBUG = False


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


@dataclass
class SimpleBlock:
    tok: Token
    val: list[Any]

    @property
    def type(self):
        return self.tok.type


@dataclass
class Function:
    name: Token
    val: list[Any]

    @property
    def type(self):
        return self.name.type


@dataclass
class Rule:
    prelude: list
    block: Optional[Any]
    location: Optional[Any] = None


@dataclass
class AtRule(Rule):
    name: str = ""


@dataclass
class QualifiedRule(Rule):
    block: list[Any] = field(default_factory=list)

    @property
    def selectors(self):
        return self.prelude


@dataclass
class Stylesheet:
    location: Optional[str]
    val: list[Rule]


@dataclass
class Declaration:
    name: str
    val: list[Token]
    important: bool = False


class CSSTokenStream:
    def __init__(self, tokens):
        self.cursor = -1
        self.tokens = tokens

    def next(self) -> Token | SimpleBlock:
        if self.cursor < len(self.tokens) - 1:
            self.cursor += 1
        else:
            return Token(type=Tok.EOF, val=None)
        return self.tokens[self.cursor]

    def reset(self) -> None:
        self.cursor = 0

    def is_only_whitespace(self) -> bool:
        return all(tok.type == Tok.WHITESPACE for tok in self.tokens)


class CSSSyntaxParser:
    input: CSSTokenStream
    reconsume_next: bool = False

    def init_state(self, inp: Any):
        self.reconsume_next = False
        if not isinstance(inp, CSSTokenStream):
            self.input = self.normalize_input(inp)
        elif self.input == inp:
            return  # called with same CSSTokenStream, don't change pointers
        else:
            self.input = inp
        self.cur, self.next = None, self.input.next()

    def normalize_input(self, inp: list | str) -> CSSTokenStream:
        if isinstance(inp, list):
            return CSSTokenStream(inp)
        if isinstance(inp, str):
            inp = (
                inp.replace("\u000d\u000a", "\n")
                .replace("\u000d", "\n")
                .replace("\u000c", "\n")
                .replace("\u0000", "\ufffd")
            )
            tokens = Lexer(inp).parse()
            return CSSTokenStream(tokens)
        return CSSTokenStream(tokens)

    # TODO: return type wrong, update later
    def consume(self) -> Token | SimpleBlock:
        if self.reconsume_next:
            self.reconsume_next = False
            return self.cur
        # load next token, return current
        self.cur = self.next
        self.next = self.input.next()
        log(f"\033[1;36m{self.cur}\033[0m")
        return self.cur

    def reconsume(self) -> None:
        self.reconsume_next = True

    def parse_error(self, msg) -> None:
        log(f"\033[0;31m{msg}\033[0m")

    # ======================== Parser Entry Points ======================== #

    # https://www.w3.org/TR/css-syntax-3/#css-stylesheets
    def parse_css_stylesheet(self, inp):  # -> list[StyleRule]:
        self.init_state(inp)
        stylesheet = self.parse_stylesheet(self.input)

        # replace each qualified rule with a StyleRule
        selector_parser = SelectorParser()
        declaration_parser = CSSSyntaxParser()
        for i in range(len(stylesheet.val)):
            stylesheet.val[i].prelude = selector_parser.parse(stylesheet.val[i].prelude)
            assert isinstance(stylesheet.val[i].block, SimpleBlock)
            contents = declaration_parser.parse_style_block_contents(
                stylesheet.val[i].block.val
            )
            print(contents)
            # if not selector_list or not contents:
            #     # style_rule.invalid = True
            #     continue

            # style_rule = StyleRule(selector_list, contents)

    def parse_comma_separated_list(self, inp) -> list:
        # parse(), but a malformed CSS item in a comma separated list will be handled correctly.
        self.init_state(inp)
        assert self.input is not None
        if self.input.is_only_whitespace():
            return []

        cvls_list = self.parse_comma_separated_component_value_list(self.input)

        # # parse each component value list according to grammar
        # parser = CSSSyntaxParser()
        # for i in range(len(cvls_list)):
        #     parser.init_state(cvls_list[i])
        #     cvls_list[i] = parser.parse()

        # # cvls_list is now a list of CSS grammar keywords
        return cvls_list

    def parse_stylesheet(self, inp, location: str = None) -> Stylesheet:
        # inp as type bytestream not in scope for this simple browser
        self.init_state(inp)
        rules = self.consume_rule_list(top_level=True)
        stylesheet = Stylesheet(location, rules)
        return stylesheet

    def parse_rules(self, inp) -> list[Rule]:
        self.init_state(inp)
        return self.consume_rule_list()

    def parse_rule(self, inp) -> Rule | None:
        self.init_state(inp)
        out = None
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type == Tok.EOF:
            self.parse_error("Error parsing rule: EOF before rule start")
            return None
        if self.next.type == Tok.AT_KEYWORD:
            out = self.consume_at_rule()
        else:
            out = self.consume_qualified_rule()
            if not out:
                self.parse_error("Error parsing rule: Could not parse a qualified rule")
                return None

        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type == Tok.EOF:
            return out
        self.parse_error("Error parsing rule: expected EOF")
        return None

    def parse_declaration(self, inp) -> Declaration | None:
        self.init_state(inp)
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type != Tok.IDENT:
            self.parse_error(
                f"Error parsing declaration: expected IDENT, but got {self.next}"
            )
            return None
        out = self.consume_declaration()
        if not out:
            self.parse_error(f"Failed to parse declaration")
            return None
        return out

    def parse_style_block_contents(self, inp) -> list[Declaration | Rule]:
        self.init_state(inp)
        return self.consume_style_block_contents()

    def parse_declaration_list(self, inp) -> list[Declaration]:
        self.init_state(inp)
        return self.consume_declaration_list()

    def parse_component_value(self, inp) -> Token | SimpleBlock | None:
        self.init_state(inp)
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type == Tok.EOF:
            self.parse_error(
                "Error parsing component value: EOF before component value start"
            )
            return None
        val = self.consume_component_value()
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type == Tok.EOF:
            return val
        self.parse_error(
            "Error parsing component value: Expected EOF after component value"
        )
        return None

    def parse_component_value_list(self, inp) -> list[Token]:
        self.init_state(inp)
        res = []
        while True:
            component_value = self.consume_component_value()
            if component_value.type == Tok.EOF:
                break
            res.append(component_value)
        return res

    def parse_comma_separated_component_value_list(self, inp) -> list[list[Token]]:
        self.init_state(inp)
        cvls_list = []
        cvls = []
        while True:
            cvl = self.consume_component_value()

            # don't add EOF or COMMA to cvls_list. if EOF is encountered, break.
            if cvl.type == Tok.EOF:
                cvls_list.append(cvls)
                break
            elif cvl.type == Tok.COMMA:
                cvls_list.append(cvls)
                cvls = []
                continue
            cvls.append(cvl)
        return cvls_list

    # ======================== Parser Helper Algorithms ======================== #

    def consume_rule_list(self, top_level=False) -> list[Rule]:
        rules = []
        while True:
            tok = self.consume()
            match tok.type:
                case Tok.WHITESPACE:
                    pass
                case Tok.EOF:
                    return rules
                case Tok.CDO, Tok.CDC:
                    if not top_level:
                        self.reconsume()
                        res = self.consume_qualified_rule()
                        if res:
                            rules.append(res)
                case Tok.AT_KEYWORD:
                    self.reconsume()
                    rules.append(self.consume_at_rule())
                case _:
                    self.reconsume()
                    res = self.consume_qualified_rule()
                    if res:
                        rules.append(res)

    def consume_at_rule(self) -> AtRule:
        self.consume()
        at_rule = AtRule(prelude=[], block=None, location=None, name=self.cur.val)
        while True:
            tok = self.consume()
            if tok.type == Tok.SEMICOLON:
                return at_rule
            if tok.type == Tok.EOF:
                self.parse_error("Error parsing at-rule: early EOF")
                return at_rule
            if isinstance(tok, SimpleBlock) and tok.type == Tok.LBRACE:
                at_rule.block = tok
                return at_rule
            if tok.type == Tok.LBRACE:
                at_rule.block = self.consume_simple_block()
                return at_rule

            self.reconsume()
            at_rule.prelude.append(self.consume_component_value())

    def consume_qualified_rule(self) -> QualifiedRule:
        qual_rule = QualifiedRule(prelude=[], block=[], location=None)
        while True:
            tok = self.consume()
            if tok.type == Tok.EOF:
                self.parse_error("Error parsing qualified rule: early EOF")
                return None
            if isinstance(tok, SimpleBlock) and tok.type == Tok.LBRACE:
                qual_rule.block = tok
                return qual_rule
            if tok.type == Tok.LBRACE:
                qual_rule.block = self.consume_simple_block()
                return qual_rule

            self.reconsume()
            qual_rule.prelude.append(self.consume_component_value())

    # returns a single list containing declarations in the order they appear,
    # followed by nested rules in the order they appear.
    def consume_style_block_contents(self) -> list[Declaration | Rule]:
        decls, rules = [], []
        while True:
            tok = self.consume()
            match tok.type:
                case Tok.WHITESPACE | Tok.SEMICOLON:
                    pass
                case Tok.EOF:
                    decls.extend(rules)
                    return decls
                case Tok.AT_KEYWORD:
                    self.reconsume()
                    rules.append(self.consume_at_rule())
                case Tok.IDENT:
                    temp = [self.cur]
                    while self.next.type not in (Tok.SEMICOLON, Tok.EOF):
                        temp.append(self.consume_component_value())
                    parser = CSSSyntaxParser()
                    parser.init_state(temp)
                    out = parser.consume_declaration()
                    if out:
                        decls.append(out)
                case Tok.DELIM if tok.val == "&":
                    self.reconsume()
                    out = self.consume_qualified_rule()
                    if out:
                        rules.append(out)
                case _:
                    self.parse_error(
                        f"Error parsing style block contents: unrecognized token {tok}"
                    )
                    self.reconsume()
                    while self.next.type not in (Tok.SEMICOLON, Tok.EOF):
                        # malformed declaration, consume entirety and throw away
                        self.consume_component_value()

    def consume_declaration_list(self) -> list[Declaration]:
        decls = []
        while True:
            tok = self.consume()
            match tok.type:
                case Tok.WHITESPACE | Tok.SEMICOLON:
                    pass
                case Tok.EOF:
                    return decls
                case Tok.AT_KEYWORD:
                    self.reconsume()
                    decls.append(self.consume_at_rule())
                case Tok.IDENT:
                    temp = [self.cur]
                    while self.next.type not in (Tok.SEMICOLON, Tok.EOF):
                        temp.append(self.consume_component_value())
                    parser = CSSSyntaxParser()
                    parser.init_state(temp)
                    decls.append(parser.consume_declaration())
                case _:
                    self.parse_error(
                        f"Error parsing declaration list: unrecognized token {tok}"
                    )
                    self.reconsume()
                    while self.next.type not in (Tok.SEMICOLON, Tok.EOF):
                        # malformed declaration, consume entirety and throw away
                        self.consume_component_value()

    def consume_declaration(self) -> Declaration:
        self.consume()
        declaration = Declaration(name=self.cur.val, val=[])
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        if self.next.type != Tok.COLON:
            self.parse_error(f"Error parsing declaration: missing ':'")
            return None
        self.consume()
        while self.next.type == Tok.WHITESPACE:
            self.consume()
        while self.next.type != Tok.EOF:
            declaration.val.append(self.consume_component_value())

        # if last two declaration.val non whitespace are DELIM(!), IDENT("important"):
        i = len(declaration.val) - 1
        while i >= 0:
            cur = declaration.val[i]
            if i > 0 and cur.type == Tok.IDENT and cur.val.lower() == "important":
                prev = declaration.val[i - 1]
                if prev.type == Tok.DELIM and prev.val == "!":
                    declaration.important = True
                    declaration.val.pop(i)
                    declaration.val.pop(i - 1)
                    i -= 1
                else:  # no whitespace allowed between '!' and 'important'
                    break
            elif cur.type != Tok.WHITESPACE:
                break
            i -= 1

        # trim trailing whitespace from declaration.val
        while declaration.val[-1].type == Tok.WHITESPACE:
            declaration.val.pop()

        return declaration

    def consume_component_value(self) -> Token | SimpleBlock:
        tok = self.consume()
        if tok.type in [Tok.LBRACE, Tok.LBRAC, Tok.LPAREN]:
            return self.consume_simple_block()
        elif tok.type == Tok.FUNCTION and not isinstance(tok, Function):
            return self.consume_function()
        return tok

    def consume_simple_block(self) -> SimpleBlock:
        mirror_end_tok = self.cur.mirror()
        # create simple block (with tok.tok_type = self.cur, val=[])
        simple_block = SimpleBlock(self.cur, [])
        while True:
            tok = self.consume()
            if tok == mirror_end_tok:
                return simple_block
            elif tok.type == Tok.EOF:
                self.parse_error("Error parsing simple block: early EOF")
                return simple_block
            else:
                self.reconsume()
                simple_block.val.append(self.consume_component_value())

    def consume_function(self) -> Function:
        func = Function(self.cur, [])
        while True:
            tok = self.consume()
            match tok.type:
                case Tok.RPAREN:
                    return func
                case Tok.EOF:
                    self.parse_error("Error parsing function: early EOF")
                    return func
                case _:
                    self.reconsume()
                    func.val.append(self.consume_component_value())


# https://www.w3.org/TR/selectors-4/#grammar
class SelectorParser:
    def __init__(self):
        self.PEEK_SIZE = 2

    def init_state(self, inp):
        self.input = CSSTokenStream(inp)
        self.stream = collections.deque(
            [self.input.next() for _ in range(self.PEEK_SIZE)]
        )
        self.cur = None

    def consume(self) -> Token | SimpleBlock:
        # load next token, return current
        self.cur = out = self.stream.popleft()
        self.stream.append(self.input.next())
        log(f"\033[95m{out}\033[0m")
        return out

    def peek(self, n: int = 1) -> Token:
        assert 1 <= n <= self.PEEK_SIZE
        return self.stream[n - 1]

    def accept(self, type: Tok = None, val=None) -> Token | bool:
        n = self.peek()
        if type and n.type != type:
            return False
        if val and n.val != val:
            return False
        return self.consume()

    def expect(self, type: Tok = None, val=None) -> None:
        if not self.accept(type=type, val=val):
            self.parse_error(
                f"Expected <{type}, val={val}> but got {self.peek()} instead"
            )

    def consume_whitespace(self) -> Token | None:
        is_whitespace = False
        while self.peek().type == Tok.WHITESPACE:
            is_whitespace = True
            self.consume()

        return Token(type=Tok.WHITESPACE, val=None) if is_whitespace else None

    def consume_until(self, type: Tok = None, val=None) -> None:
        while True:
            n = self.peek()
            if n.type == type:
                if n.val == val or not val:
                    return
            if n.type == Tok.EOF:
                return
            self.consume()

    def parse_error(self, msg="") -> None:
        log(f"\033[91m{msg if msg else "Parse Error at"}\033[0m")

    # ======================== Parse Left Hand Rules ======================== #

    def parse(self, inp):
        self.init_state(inp)

        log("Selector Parser input tokens:", self.input.tokens)

        selector_list = self.parse_selector_list()
        log("\nSelector list:", selector_list)
        return selector_list

    def parse_selector_list(self) -> list[Selector]:
        return self.parse_complex_selector_list()

    def parse_complex_selector_list(self) -> list[ComplexSelector]:
        out = [self.parse_complex_selector()]
        while True:
            self.consume_whitespace()
            if not self.accept(type=Tok.COMMA):
                return out
            self.consume_whitespace()
            out.append(self.parse_complex_selector())

    # <compound-selector>#
    # not used by any other rhs rule
    def parse_compound_selector_list(self) -> list[CompoundSelector]:
        out = [self.parse_compound_selector()]
        while True:
            self.consume_whitespace()
            if not self.accept(type=Tok.COMMA):
                return out
            self.consume_whitespace()
            out.append(self.parse_compound_selector())

    # <simple-selector>#
    # not used by any other rhs rule
    def parse_simple_selector_list(self) -> list[SimpleSelector]:
        out = [self.parse_simple_selector()]
        while True:
            self.consume_whitespace()
            if not self.accept(type=Tok.COMMA):
                return out
            self.consume_whitespace()
            out.append(self.parse_simple_selector())

    # <relative-selector>#
    # not used by any other rhs rule
    def parse_relative_selector_list(self) -> list[ComplexSelector]:
        out = [self.parse_relative_selector()]
        while True:
            self.consume_whitespace()
            if not self.accept(type=Tok.COMMA):
                return out
            self.consume_whitespace()
            out.append(self.parse_relative_selector())

    def parse_complex_selector(self) -> ComplexSelector:
        invalid = False

        selectors = collections.deque([self.parse_compound_selector()])
        while True:
            whitespace = self.consume_whitespace()
            if self.is_combinator():
                comb = self.parse_combinator()
                self.consume_whitespace()
            elif whitespace:
                comb = Combinator.DESCENDANT

            if self.is_compound_selector():
                selectors.append(comb)
                selectors.append(self.parse_compound_selector())
            else:
                # self.parse_error(
                #     f"Error while parsing complex selector: expected compound selector after combinator"
                # )
                break

        # selectors = [Compound0, Combinator1, Compound1, Combinator2, ...]
        # combine into [Compound0(), Compound1(Combinator1), ...]
        compound_selectors = [selectors.popleft()]
        while selectors:
            comb = selectors.popleft()
            s = selectors.popleft()
            s.combinator = comb
            compound_selectors.append(s)

        out = ComplexSelector(compound_selectors=compound_selectors)
        out.invalid = invalid
        return out

    # <combinator>? <complex-selector>
    # not used by any other rhs rule
    def parse_relative_selector(self) -> tuple[Combinator, ComplexSelector]:
        comb = Combinator.NONE
        if self.is_combinator():
            comb = self.parse_combinator()
        return comb, self.parse_complex_selector()

    # [ <type-selector>? <subclass-selector>*
    # [ <pseudo-element-selector> <pseudo-class-selector>* ]* ]!
    # TODO apply semantic restrictions on pseudo element/class positions
    def parse_compound_selector(self) -> CompoundSelector:
        selectors = []
        pseudo_elements = []
        if self.is_type_selector():
            selectors.append(self.parse_type_selector())

        while self.is_subclass_selector():
            selectors.append(self.parse_subclass_selector())

        # [ <pseudo-element-selector> <pseudo-class-selector>* ]*
        while self.peek().type == Tok.COLON:
            if self.peek(2).type == Tok.COLON:
                pseudo_elements.append(self.parse_pseudo_element_selector())

            if pseudo_elements:
                # consume any amount of pseudo-class-selectors
                while (
                    self.peek(2).type == Tok.IDENT or self.peek(2).type == Tok.FUNCTION
                ):
                    pseudo_elements[-1].pseudo_classes.append(
                        self.parse_pseudo_class_selector()
                    )
            else:
                self.parse_error(
                    "':' present on selector, but no Pseudo Element found immediately after"
                )
                break

        return CompoundSelector(selectors, pseudo_elements)

    def parse_simple_selector(self) -> SimpleSelector:
        if self.is_type_selector():
            return self.parse_type_selector()
        if self.is_subclass_selector():
            return self.parse_subclass_selector()
        self.parse_error(
            f"Error while parsing simple selector, expected type or subclass selector"
        )

    def parse_combinator(self) -> Combinator:
        comb = self.consume()
        assert comb.type == Tok.DELIM
        if comb.val == ">":
            return Combinator.CHILD
        if comb.val == "+":
            return Combinator.NEXT_SIBLING
        if comb.val == "~":
            return Combinator.SUBSEQUENT_SIBLING
        if comb.val == "|":
            peek = self.peek()
            if peek.type == Tok.DELIM and peek.val == "|":
                self.consume()
                return Combinator.COLUMN
            else:
                self.parse_error(f"Expected || but got |{self.peek()}")
                return None
        self.parse_error(f"Failed to parse combinator {comb}")

    # <wq-name> | <ns-prefix>? '*'
    def parse_type_selector(self) -> TypeSelector | UniversalSelector:
        tok = self.peek()
        if self.is_wq_name():
            namespace, name = self.parse_wq_name()
            return TypeSelector(name, namespace)
        else:
            out = UniversalSelector()
            if self.is_ns_prefix():
                out.namespace = self.parse_ns_prefix()
            self.expect(type=Tok.DELIM, val="*")
            return out

    # [ <ident-token> | '*' ]? '|'
    def parse_ns_prefix(self) -> str:
        tok = self.peek()
        if tok.type == Tok.DELIM and tok.val == "|":
            self.consume()
            return ""
        if tok.type == Tok.IDENT:
            return self.consume().val
        elif tok.type == Tok.DELIM and tok.val == "*":
            return self.consume().val
        self.parse_error(f"Error parsing ns-prefix: {tok}")
        return None

    # <ns-prefix>? <ident-token>
    def parse_wq_name(self) -> tuple[str, str]:
        namespace = ""
        if self.is_ns_prefix():
            namespace = self.parse_ns_prefix()

        ident = self.consume()
        if ident.type != Tok.IDENT:
            self.parse_error("Expected IDENT token")
        return namespace, ident.val

    # <id-selector> | <class-selector> | <attribute-selector> | <pseudo-class-selector>
    def parse_subclass_selector(self) -> SimpleSelector:
        tok = self.peek()
        if tok.type == Tok.HASH:
            return self.parse_id_selector()
        if tok.val == ".":
            return self.parse_class_selector()
        if tok.type == Tok.LBRAC:
            return self.parse_attribute_selector()
        if tok.type == Tok.COLON:
            return self.parse_pseudo_class_selector()
        self.parse_error(
            "Error while parsing subclass: expected <id-selector> | <class-selector> | <attribute-selector> | <pseudo-class-selector>"
        )

    def parse_id_selector(self) -> IDSelector:
        hash_tok = self.consume()
        return IDSelector(hash_tok.val)

    def parse_class_selector(self) -> ClassSelector:
        self.expect(type=Tok.DELIM, val=".")
        ident = self.accept(type=Tok.IDENT)
        if not ident:
            self.parse_error(
                f"Error while parsing class selector: Expected ident, but got {self.peek()}"
            )
            return None
        return ClassSelector(ident.val)

    # '[' <wq-name> ']' |
    # '[' <wq-name> <attr-matcher> [ <string-token> | <ident-token> ] <attr-modifier>? ']'
    def parse_attribute_selector(self) -> AttributeSelector:
        block = self.consume()
        assert isinstance(block, SimpleBlock)

        # fork token stream over to child parser
        parser = SelectorParser()
        parser.init_state(block.val)
        out = parser._parse_attribute_selector()
        log(out)
        return out

    # TO BE CALLED FROM parse_attribute_selector ONLY!!!
    def _parse_attribute_selector(self):
        self.consume_whitespace()

        namespace, attr = self.parse_wq_name()
        self.consume_whitespace()

        if self.peek().type == Tok.EOF:
            self.consume()
            return AttributeSelector(attr, AttributeMatch.HAS_ATTR, namespace=namespace)

        matcher = self.parse_attr_matcher()
        self.consume_whitespace()
        val = ""
        if self.peek().type == Tok.STRING:
            val = self.consume().val
        elif self.peek().type == Tok.IDENT:
            val = self.consume().val
        else:
            self.parse_error(
                f"Error while parsing attribute selector: expected a rhs value but got {self.peek()}"
            )
        self.consume_whitespace()

        modifier = ""
        if not self.peek().type == Tok.EOF:
            modifier = self.parse_attr_modifier()

        return AttributeSelector(
            attr, matcher, val=val, modifier=modifier, namespace=namespace
        )

    def parse_attr_matcher(self) -> AttributeMatch:
        tok = self.peek()
        out = AttributeMatch.HAS_ATTR
        if tok.type == Tok.DELIM:
            match tok.val:
                case "=":
                    self.consume()
                    return AttributeMatch.EXACT_MATCH
                case "~":
                    out = AttributeMatch.CONTAINS_WORD
                case "*":
                    out = AttributeMatch.CONTAINS_STRING
                case "|":
                    out = AttributeMatch.DASH_END
                case "^":
                    out = AttributeMatch.PREFIX_MATCH
                case "$":
                    out = AttributeMatch.SUFFIX_MATCH
                case _:
                    self.parse_error(
                        f"Error while parrsing attribute matcher: {self.peek()} is not a valid matcher (_, =, ~=, *=, |=, ^=, $=)"
                    )
                    return None
            self.consume()
            self.consume()
            return out

    def parse_attr_modifier(self) -> str:
        tok = self.peek()
        if tok.type == Tok.IDENT and (tok.val == "i" or tok.val == "s"):
            return tok.val
        self.parse_error(
            f"Error parsing attribute modifier, '{tok.val}' must be either 'i' or 's'"
        )
        return ""

    #':' <ident-token> | ':' <function-token> <any-value> ')'
    def parse_pseudo_class_selector(self) -> PseudoClassSelector:
        self.expect(type=Tok.COLON)
        tok = self.peek()
        if tok.type == Tok.IDENT:
            ident = self.consume()
            return PseudoClassSelector(ident.val.lower(), None)
        elif tok.type == Tok.FUNCTION:
            func = self.consume()
            assert isinstance(func, Function)
            return PseudoClassSelector(func.name.val, func.val)
        else:
            self.parse_error(
                f"Error while parsing pseudo class selector: Expected either ident or function, got {self.peek()}"
            )
            return None

    def parse_pseudo_element_selector(self) -> PseudoElement:
        self.expect(type=Tok.COLON)
        pseudo_class = self.parse_pseudo_class_selector()
        return PseudoElement(
            name=pseudo_class.name.lower(), args=pseudo_class.args, pseudo_classes=[]
        )

    # ======================== Parser Lookahead Helper Algorithms ======================== #

    def is_compound_selector(self) -> bool:
        tok = self.peek()
        return (
            self.is_type_selector()
            or self.is_subclass_selector()
            or self.is_pseudo_element_selector()
        )

    def is_type_selector(self) -> bool:
        tok = self.peek()
        return (
            self.is_wq_name()
            or self.is_ns_prefix()
            or tok.type == Tok.DELIM
            and tok.val == "*"
        )

    def is_wq_name(self) -> bool:
        tok = self.peek()
        return self.is_ns_prefix() or tok.type == Tok.IDENT

    def is_ns_prefix(self) -> bool:
        tok = self.peek()
        tok2 = self.peek(2)
        if tok.type == Tok.IDENT or tok.type == Tok.DELIM and tok.val == "*":
            return tok2.type == Tok.DELIM and tok2.val == "|"
        return tok.type == Tok.DELIM and tok.val == "|"

    def is_combinator(self) -> bool:
        tok = self.peek()
        if tok.type == Tok.DELIM:
            if len(tok.val) == 1 and tok.val in ">+~":
                return True
            elif tok.val == "||":
                return True
        return False

    def is_subclass_selector(self) -> bool:
        tok = self.peek()
        if tok.type == Tok.HASH or tok.type == Tok.LBRAC:
            return True
        if tok.type == Tok.COLON:
            return self.peek(2).type != Tok.COLON  # is a pseudo element ::
        if tok.type == Tok.DELIM and tok.val == ".":
            return True
        return False

    def is_pseudo_element_selector(self) -> bool:
        tok = self.peek()
        return tok.type == Tok.COLON


if __name__ == "__main__":
    import sys

    DEBUG = True

    f = "./browser.css"
    if len(sys.argv) > 1:
        f = sys.argv[1]

    with open(f, "r") as file:
        lexer = Lexer(file.read())
        tokens = lexer.parse()

        # for token in lexer.parse():
        #     print(token)
        # print_sheet(file.read())

        parser = CSSSyntaxParser()
        # parser.init_state(tokens)
        # parser.consume()
        # parser.reconsume()
        # parser.consume()
        # parser.consume()

        stylesheet = parser.parse_css_stylesheet(tokens)
        # stylesheet = parser.parse_stylesheet(tokens)
        # print(stylesheet)
