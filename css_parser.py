from html_parser import Element

class TagSelector:
    def __init__(self, tag):
        self.tag = tag
        
    def __repr__(self):
        return self.tag

    def matches(self, node):
        return isinstance(node, Element) and self.tag == node.tag
    
class DescendantSelector:
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant
        
    def __repr__(self):
        # collect tags from the chain into a stack (right-to-left)
        parts = []
        cur = self
        while isinstance(cur, DescendantSelector):
            parts.append(cur.descendant.tag)
            cur = cur.ancestor
        # cur is now a TagSelector; include its tag
        parts.append(cur.tag)
        parts.reverse()
        return " ".join(parts)
    
    def matches(self, node):
        if not self.descendant.matches(node): return False
        while node.parent:
            if self.ancestor.matches(node.parent): return True
            node = node.parent
        return False

class CSSParser:
    def __init__(self, s):
        self.s = s
        self.i = 0
    
    def whitespace(self):
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1
            
    def word(self):
        res = []
        start = self.i
        while self.i < len(self.s):
            if self.s[self.i].isalnum() or self.s[self.i] in "#-.%":
                res.append(self.s[self.i])
                self.i += 1
            elif self.s.startswith("/*", self.i): # ignore comments
                self.ignore_until(["*/"])
                self.i += 2
                self.whitespace()
            else:
                break
        if not self.i > start:
            raise Exception("Parsing error")
        return ''.join(res)

    def literal(self, literal):
        if not (self.i < len(self.s) and self.s[self.i] == literal):
            raise Exception(f"Parsing error: Expected literal {literal} but saw {self.s[self.i]} instead")
        self.i += 1
    
    def pair(self):
        prop = self.word()
        self.whitespace()
        self.literal(":")
        self.whitespace()
        val = self.word()
        return prop.casefold(), val

    def body(self):
        pairs = {}
        while self.i < len(self.s) and self.s[self.i] != "}":
            try:
                prop, val = self.pair()
                pairs[prop] = val
                self.whitespace()
                self.literal(";")
                self.whitespace()
            except Exception:
                why = self.ignore_until([';', '}'])
                if why == ";":
                    self.literal(";")
                    self.whitespace()
                else:
                    break
        return pairs

    def ignore_until(self, chars):
        while self.i < len(self.s):
            for char in chars:
                if self.s.startswith(char, self.i):
                    return char
            self.i += 1
        return None
    
    def selector(self):
        out = TagSelector(self.word().casefold())
        self.whitespace()
        while self.i < len(self.s) and self.s[self.i] != "{":
            tag = self.word()
            descendant = TagSelector(tag.casefold())
            out = DescendantSelector(out, descendant)
            self.whitespace()
        return out
    
    def parse(self):
        rules = []
        while self.i < len(self.s):
            try:
                self.whitespace()
                selector = self.selector()
                self.literal("{")
                self.whitespace()
                body = self.body()
                self.literal("}")
                rules.append((selector, body))
            except Exception:
                why = self.ignore_until(['}'])
                if why == "}":
                    self.literal("}")
                    self.whitespace()
                else:
                    break
        return rules

def style(node, rules):
    node.style = {}
    
    # style sheet rules
    for selector, body in rules:
        if not selector.matches(node): continue
        for prop, value in body.items():
            node.style[prop] = value
            
    # style attribute rules
    if isinstance(node, Element) and "style" in node.attributes:
        pairs = CSSParser(node.attributes["style"]).body()
        for property, value in pairs.items():
            node.style[property] = value
    
    for child in node.children:
        style(child, rules)

def print_sheet(s):
    parser = CSSParser(s)
    res = parser.parse()
    for selector, rules in res:
        print(selector)
        for prop, value in rules.items():
            print(f"    {prop}: '{value}'")
        print()
        
def print_rules(r):
    for selector, rules in r:
        print(selector)
        for prop, value in rules.items():
            print(f"    {prop}: '{value}'")
        print()

if __name__ == "__main__":
    import sys
    f = "./browser.css"
    if len(sys.argv) > 1:
        f = sys.argv[1]
    
    with open(f, 'r') as file:
        print_sheet(file.read())