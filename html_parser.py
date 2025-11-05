SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

HEAD_TAGS = [
    "base", "basefont", "bgsound", "noscript",
    "link", "meta", "title", "style", "script",
]

class Text:
    def __init__(self, text, parent):
        self.text = text
        self.children = []
        self.parent = parent
        
    def __repr__(self):
        return repr(self.text)
    
class Element:
    def __init__(self, tag, attributes, parent):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.parent = parent
        
    def __repr__(self):
        return "<" + self.tag + ">"
            
class HTMLParser:
    def __init__(self, body):
        self.body = body
        self.unfinished = []

    def parse(self):
        text = []
        in_tag = False
        in_script = False
        i = 0
        while i < len(self.body):
            c = self.body[i]
            if c == "&" and not in_tag:
                # handle entities
                if self.body[i+1:i+4] == "lt;":
                    c = "<"
                    i += 3
                elif self.body[i+1:i+4] == "gt;":
                    c = ">"
                    i += 3
                elif self.body[i+1:i+5] == "shy;":
                    c = "\u00AD"
                    i += 4
                text.append(c)

            elif c == "<":
                if self.body[i+1:i+4] == "!--":
                    # if comment, jump to end of comment
                    i += 3
                    while self.body[i:i+3] != "-->":
                        i += 1
                    i += 3
                    continue
                else:
                    # flush buffer contents
                    in_tag = True
                    if text:
                        self.add_text(''.join(text))
                    text = []
            elif c == ">":
                in_tag = False
                tag = ''.join(text)
                self.add_tag(tag)
                text = []
                
                if tag == "script":
                    # jump to matching </script> tag, add text to tag
                    start = i
                    while self.body[i:i+9] != "</script>":
                        i += 1
                    self.add_text(self.body[start+1:i])
                    self.add_tag('/script')
                    i += 9
                    continue
            else:
                text.append(c)
            i += 1
        if not in_tag and text:
            self.add_text(''.join(text))
        
        return self.finish()
    
    def add_text(self, text):
        if text.isspace(): return
        self.implicit_tags(None)
        # add text to last unfinished node
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)
    
    def add_tag(self, tag):
        tag, attributes = self.get_attributes(tag)
        if tag.startswith("!"): return
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            # finish previous node
            # not creating a closing tag, just marking an opening one as finished
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in SELF_CLOSING_TAGS:
            # add an already finished tag
            parent = self.unfinished[-1]
            node = Element(tag, attributes, parent)
            parent.children.append(node)
        else:
            # add unfinished node to prev unfinished node
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, attributes, parent)
            self.unfinished.append(node)
            # don't add to parent's children[] here, we only do that once it's closed
    
    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
        # finish all remaining nodes (add to parent's children)
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()

    def get_attributes(self, text):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, val = attrpair.split("=", 1)
                if len(val) > 2 and val[0] in ["'", '"']: # strip quotes from value
                    val = val[1:-1]
                attributes[key.casefold()] = val
            else:
                attributes[attrpair.casefold()] = ""
        return tag, attributes
        
    def implicit_tags(self, tag):
        while True:
            # if no tags yet, and tag isn't html, insert html
            if not self.unfinished:
                if tag == "html":
                    break
                self.add_tag("html")
            
            top = self.unfinished[-1].tag
            
            # if html, but encounter a tag that belongs to either head or body:
            if top == "html" and tag not in ("head", "body", "/html"):
                if tag in HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
                continue
            
            # html + head, but encounter something that should be in body
            if top == "head" and len(self.unfinished) >= 2 and self.unfinished[-2].tag == "html" and \
                    tag not in HEAD_TAGS and tag != "/head":
                self.add_tag("/head")
                continue

            # nested paragraphs: in a <p>, and see another <p>
            if top == "p" and tag == "p":
                self.add_tag("/p")
                continue
            
            # nested lists: in a <li>, and see another <li>
            if top == "li" and tag != "/li":
                self.add_tag("/li")
                continue

            break
            
            
def print_tree(node, indent=0):
    print("." * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

if __name__ == "__main__":
    from url import URL
    import sys
    url = "file:///home/yuzu/Documents/browser-dev/parsetest"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    body = URL(url).request()
    nodes = HTMLParser(body).parse()
    print_tree(nodes)