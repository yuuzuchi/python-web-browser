from html_parser import Element, Text
from dataclasses import dataclass, field

DEBUG = False

INHERITED_PROPERTIES = {
    "font-size": "16px",
    "font-style": "normal",
    "font-weight": "normal",
    "font-family": "Crimson Pro",
    "color": "black",

    "white-space": "normal",
}

# font shorthand keywords
STYLE = {"italic", "oblique"}
VARIANT = {"small-caps"}
WEIGHT = {"bold", "bolder", "lighter"}
STRETCH = {"condensed", "expanded", "semi-condensed", "extra-condensed", "extra-expanded", "ultra-condensed", "ultra-expanded"}
SIZE = {"px", "pt", "em", "rem", "%", "vh", "vw"}

class Selector:
    def __init__(self, specificity: tuple[int, int, int]):
        """(num_ids, num_classes, num_tags) - for priority calculation"""
        self.specificity = specificity 

class TagSelector(Selector):
    def __init__(self, tag: str):
        super().__init__((0, 0, 1))
        self.tag = tag
        
    def __str__(self):
        return self.tag

    def matches(self, node: Element | Text):
        return isinstance(node, Element) and self.tag == node.tag
    
class ClassSelector(Selector):
    def __init__(self, clss: str):
        classes = clss.split(".")[1:] # ignore leading dot
        super().__init__((0, len(classes), 0))
        self.clss = clss
        self.classes = classes
        
    def __str__(self):
        return self.clss
        
    def matches(self, node: Element | Text):
        if not isinstance(node, Element):
            return False
        for clss in self.classes:
            if not clss in node.classes:
                return False
        return True

class SelectorSequence(Selector):
    def __init__(self, tag: TagSelector, clss: ClassSelector):
        combined = tuple(a + b for a, b in zip(tag.specificity, clss.specificity))
        super().__init__(combined)
        self.tag = tag
        self.clss = clss
        self.selector = f"{self.tag.tag}{self.clss.clss}"
        
    def __str__(self):
        return self.selector
    
    def matches(self, node: Element | Text):
        return self.tag.matches(node) and self.clss.matches(node)

class DescendantSelector(Selector):
    def __init__(self, selector: Selector):
        super().__init__(selector.specificity)
        self.selector_list = [selector]
        
    def __str__(self):
        return " ".join([str(selector) for selector in self.selector_list])
    
    def add_right(self, selector: Selector):
        self.selector_list.append(selector)
        self.specificity = tuple(a + b for a, b in zip(self.specificity, selector.specificity))

    def matches(self, node: Element | Text):
        def _matches(node: Element | Text, idx):
            while idx >= 0 and node:
                if self.selector_list[idx].matches(node):
                    idx -= 1
                node = node.parent
            return idx < 0
        return _matches(node, len(self.selector_list)-1)
    
class HasSelector(Selector):
    def __init__(self, target: Selector | None, selector_list: list[Selector]): 
        parens_specificity = max(selector.specificity for selector in selector_list) if selector_list else (0, 0, 0)
        target_specificity = target.specificity if target else (0, 0, 0)
        combined = tuple(a + b for a, b in zip(parens_specificity, target_specificity))
        super().__init__(combined) # take max specificity within 
        self.target = target
        self.selector_list = selector_list
    
    def __str__(self):
        return f"{str(self.target) if self.target else ""}:has({", ".join([str(selector) for selector in self.selector_list])})"
    
    def set_selectors(self, selector_list: list[Selector]):
        self.selector_list = selector_list
        parens_specificity = max(selector.specificity for selector in selector_list) if selector_list else (0, 0, 0)
        target_specificity = self.target.specificity if self.target else (0, 0, 0)
        self.specificity = tuple(a + b for a, b in zip(parens_specificity, target_specificity))

    # a proper implementation would walk right to left and call a restyle on matched parents
    # but I'll skip this optimization for small static sites
    def matches(self, node): 
        if self.target and not self.target.matches(node):
            return False
        return self._match_child(node)

    def _match_child(self, node):
        # check if any [selectors] are in node's children
        if node and isinstance(node, Element):
            for child in node.children:
                for selector in self.selector_list:
                    if selector.matches(child): return True
                if self._match_child(child): return True
        return False
        

@dataclass
class Declaration:
    prop: str
    val: str
    important: bool
    origin_priority: int
    rule_order: int
    sort_key: tuple | None = field(default=None, init=False)
    
    def with_specificity(self, specificity):
        decl = Declaration(self.prop, self.val, self.important, self.origin_priority, self.rule_order)
        decl.sort_key = (self.important, self.origin_priority, specificity, self.rule_order)
        return decl
    
    def set_specificity(self, specificity):
        self.specificity = specificity
        self.sort_key = (self.important, self.origin_priority, specificity, self.rule_order)

    def __str__(self):
        return f"{self.prop}: {self.val}{" !important" if self.important else ""};"

@dataclass
class Rule:
    selector: Selector
    declarations: list[Declaration]

    def __str__(self):
        return f"{str(self.selector)}\n{"\n".join("  " + str(decl) for decl in self.declarations)}"

class CSSParser:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.decl_count = 0
    
    def whitespace(self):
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1
        self.comment()
    
    def comment(self):
        if self.i < len(self.s) and self.s.startswith("/*", self.i):
            self.consume_until(["*/"])
            self.i += 2
            self.whitespace()
            
    def word(self, is_selectors=False):
        res = []
        start = self.i
        while self.i < len(self.s):
            if is_selectors:
                # all for :has() tag - split :has and () into two different word() calls
                if self.s[self.i].isalnum() or self.s[self.i] in "@#.:":
                    res.append(self.s[self.i])
                    self.i += 1
                else:
                    break
            else:
                if self.s[self.i].isalnum() or self.s[self.i] in "!@#-.%":
                    res.append(self.s[self.i])
                    self.i += 1
                elif self.s[self.i] == "/" and self.i == start:
                    res.append(self.s[self.i])
                    self.i += 1
                    self.whitespace()
                else:
                    break

        if not self.i > start:
            raise Exception("Parsing error: no words parsed")
        return ''.join(res)

    def literal(self, literal):
        if not (self.i < len(self.s) and self.s[self.i] == literal):
            raise Exception(f"Parsing error: Expected literal {literal}")
        self.i += 1
    
    def string(self):
        if not (self.i < len(self.s) and self.s[self.i] in ("'", '"')):
            raise Exception("Parsing error: not at string start")
        quote = self.s[self.i]
        self.i += 1
        res = []
        while self.i < len(self.s):
            self.comment()
            c = self.s[self.i]
            if c == '\\':
                self.i += 1
                if self.i < len(self.s):
                    res.append(self.s[self.i])
                    self.i += 1
                else:
                    raise Exception("unterminated escape in string")
            elif c == quote:
                self.i += 1
                return ''.join(res)
            else:
                res.append(c)
                self.i += 1
        raise Exception("Parsing error: unterminated string")

    def value(self) -> tuple[str, bool]:
        out = []
        important = False
        while self.i < len(self.s) and self.s[self.i] not in ";}":
            # parse string or word until semicolon
            if self.s[self.i] in ("'", '"'):
                out.append(self.string())
            else:
                word = self.word()
                if word != "!important":
                    out.append(word)
                    important = False # !important must be the last value
                else:
                    important = True
            self.whitespace()
        return out, important

    def pair(self) -> tuple[str, list, bool]:
        prop = self.word()
        self.whitespace()
        self.literal(":")
        self.whitespace()
        val, important = self.value()
        return prop, val, important

    def body(self, origin_priority, specificity=None) -> list[Declaration]:
        declarations = []
        while self.i < len(self.s) and self.s[self.i] != "}":
            try:
                prop, vals, important = self.pair()
                if prop == "font":
                    pairs = self._font_shorthand(vals)
                    
                    # add all pairs as new declarations
                    for prop, val in pairs.items():
                        decl = Declaration(prop, val, important, origin_priority, self.decl_count)
                        if specificity: decl.set_specificity(specificity)
                        declarations.append(decl)
                else:
                    if len(vals) == 1: val = vals[0]
                    decl = Declaration(prop, val, important, origin_priority, self.decl_count)
                    if specificity: decl.set_specificity(specificity)
                    declarations.append(decl)
                
                self.decl_count += 1
                self.whitespace()
                self.literal(";")
                self.whitespace()
            except Exception as e:
                if DEBUG: print("Body,", e)
                why = self.consume_until([';', '}'])
                if why == ";":
                    self.literal(";")
                    self.whitespace()
                else:
                    break
        return declarations

    def consume_until(self, chars):
        while self.i < len(self.s):
            for char in chars:
                if self.s.startswith(char, self.i):
                    return char
            self.i += 1
        return None
    
    def parens(self) -> list[Selector]:
        res = []
        if self.i < len(self.s) and self.s[self.i] == "(":
            self.i += 1
            self.whitespace()
            while self.i < len(self.s) and self.s[self.i] != ")":
                res.append(self.selector())
                if self.s[self.i] == ",":
                    self.literal(",")
                else:
                    break
                self.whitespace()
        self.literal(")")
        self.whitespace()
        return res
    
    def selector(self) -> Selector:
        out = self._one_selector()
        if isinstance(out, HasSelector):
            out.set_selectors(self.parens())

        first = True
        self.whitespace()
        while self.i < len(self.s) and self.s[self.i] not in "{,)":            
            nxt = self._one_selector()
            if isinstance(nxt, HasSelector):
                nxt.set_selectors(self.parens())

            if first:
                first = False
                out = DescendantSelector(out)
            out.add_right(nxt)
            self.whitespace()
        return out
    
    def _one_selector(self) -> Selector | None:
        def get_selector(text):
            if "." in text:
                if text.startswith("."):
                    return ClassSelector(text)
                else:
                    parts = text.split(".", 1)
                    return SelectorSequence(
                        TagSelector(parts[0]),
                        ClassSelector("." + parts[1])
                    )
            return TagSelector(text)

        selector = self.word(is_selectors=True).casefold()
        if ":" in selector:
            parts = selector.split(":")
            if parts[0] != "":
                return HasSelector(get_selector(parts[0]), [])
            return HasSelector(None, [])
        else:
            return get_selector(selector)
    
    def selectors(self) -> list[Selector]:
        out = []
        while self.i < len(self.s):
            selector = self.selector()
            out.append(selector)
            self.whitespace()
        
            if self.i >= len(self.s) or self.s[self.i] == "{":
                break

            self.literal(",")
            self.whitespace()
        return out
    
    def parse(self, origin_priority, s=None) -> list[Rule]: # if passed s argument, reset s and i for new text
        if s:
            self.s = s
            self.i = 0
            
        rules = []
        self.whitespace()
        while self.i < len(self.s):
            try:
                selectors = self.selectors()
                self.literal("{")
                self.whitespace()
                body = self.body(origin_priority)
                self.literal("}")
                for selector in selectors:
                    body_copy = [decl.with_specificity(selector.specificity) for decl in body]
                    rules.append(Rule(selector, body_copy))
                self.whitespace()
            except Exception as e:
                if DEBUG: print("Parse,", e)
                why = self.consume_until(['}'])
                if why == "}":
                    self.literal("}")
                    self.whitespace()
                else:
                    break
        return rules
    
    def _font_shorthand(self, val):
        # default values
        pairs = {
            'font-style': 'normal', 
            'font-variant': 'normal', 
            'font-weight': 'normal',
            'font-stretch': 'normal',
            'line-height': '1.5'
        }
        # look for font-size (mandatory), ends with size unit
        size_idx = -1
        for i in range(len(val)):
            for unit in SIZE:
                if val[i].endswith(unit):
                    pairs['font-size'] = val[i]
                    size_idx = i
        # match style, variant, weight, stretch before size_idx
        for i in range(size_idx):
            if val[i] in STYLE:         
                pairs['font-style'] = val[i]
            elif val[i] in VARIANT:     
                pairs['font-variant'] = val[i]
            elif val[i] in WEIGHT:
                pairs['font-weight'] = val[i]
            elif val[i].isdigit():
                pairs['font-weight'] = int(val[i])
            elif val[i] in STRETCH:
                pairs['font-stretch'] = val[i]
        # line-height
        if size_idx < len(val)-2:
            pairs['line-height'] = float(val[size_idx+1][1:])
        pairs['font-family'] = val[-1]
        return pairs

# To style the entire node tree, we need to do two passes
# First pass to read all <style> tags and add them to our rules
# Second to actually compute styles for each node
# Time complexity: 
def style(node, rules, parser: CSSParser):
    def parse_styletags(node):
        if isinstance(node, Text) and node.parent.tag == "style":
            styletag_rules = parser.parse(origin_priority=2, s=node.text)
            rules.extend(styletag_rules)
            
        for child in node.children:
            parse_styletags(child)

    def _style(node):
        candidates = []
        # get sheet rules
        for rule in rules:
            selector, declarations = rule.selector, rule.declarations
            if not selector.matches(node): continue
            candidates.extend(declarations)
                
        # get any style attribute rules
        if isinstance(node, Element) and "style" in node.attributes:
            declarations = CSSParser(node.attributes["style"]).body(3, specificity=(0,0,0))
            candidates.extend(declarations)
            
        # add styles to nodes
        final = {}
        for decl in candidates:
            prop = decl.prop
            if prop not in final or decl.sort_key > final[prop].sort_key:
                final[prop] = decl
            
        # replace decl objects with their values
        node.style = {prop: decl.val for prop, decl in final.items()}

        # get inheritable properties from parents
        for prop, default in INHERITED_PROPERTIES.items():
            if prop in final:
                continue
            elif node.parent:
                node.style[prop] = node.parent.style[prop]
            else:
                node.style[prop] = default
                
        _compute(node)
        
        for child in node.children:
            _style(child)
    
    parse_styletags(node) 
    _style(node)   


        
def _compute(node):
    # resolve 'inherit' and related keywords
    for prop, value in node.style.items():
        if value == "inherit":
            node.style[prop] = node.parent.style[prop]
        elif value == "initial":
            # node.style[prop] = INHERITED_PROPERTIES[prop]
            del node.style[prop]
        elif value == "unset":
            if prop in INHERITED_PROPERTIES:
                node.style[prop] = node.parent.style[prop]
            else:
                del node.style[prop]
                
    # compute font shorthand (font-size and font-family are required
    # font: [font-style] [font-variant] [font-weight] [font-stretch] font-size [/ line-height] font-family
    if "font" in node.style:
        pass
                    
    # compute percentages to px values (to prevent inherited fonts from scaling off of parents again)
    if node.style["font-size"].endswith("%"):
        if node.parent:
            parent_font_size = node.parent.style['font-size']
        else:
            parent_font_size = INHERITED_PROPERTIES["font-size"]
        node_pct = float(node.style["font-size"][:-1]) / 100
        parent_px = float(parent_font_size[:-2])
        node.style["font-size"] = str(node_pct * parent_px) + "px"
        
def print_sheet(s):
    parser = CSSParser(s)
    res = parser.parse(1)
    for rule in res:
        print(str(rule))
        print()
        
def print_rules(rules):
    for rule in rules:
        print(str(rule))
        print()

if __name__ == "__main__":
    DEBUG = True
    import sys
    f = "./browser.css"
    if len(sys.argv) > 1:
        f = sys.argv[1]
    
    with open(f, 'r') as file:
        print_sheet(file.read())