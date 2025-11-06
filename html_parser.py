SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

HEAD_TAGS = [
    "base", "basefont", "bgsound", "noscript",
    "link", "meta", "title", "style", "script",
]

FORMAT_TAGS = [
    "b", "strong", "i", "em", "mark", "small", "big", "del", "ins", "sub", "sup"
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
        return f"<{self.tag}{str(self.attributes) if self.attributes else ""}>"
            
class HTMLParser:
    def __init__(self, body):
        self.body = body
        self.unfinished = []

    def parse(self):
        text = []
        in_tag = False
        in_attribute = False # quoted attributes may contain <, >, and space
        quote = None # either " or ' or None
        i = 0
        n = len(self.body)
        
        while i < n:
            c = self.body[i]
            
            # handle entities
            if c == "&" and not in_tag:
                if self.body.startswith("lt;", i+1):
                    text.append("<")
                    i += 4
                    continue
                elif self.body.startswith("gt;", i+1):
                    text.append(">")
                    i += 4
                    continue
                elif self.body.startswith("quot;", i+1):
                    text.append('"')
                    i += 6
                    continue
                elif self.body.startswith("#39;", i+1):
                    text.append("'")
                    i += 5
                    continue
                elif self.body.startswith("shy;", i+1):
                    text.append("\u00AD")
                    i += 5
                    continue
                text.append(c)
                    
            elif c == "<" and not in_tag and not in_attribute:
                # if comment, jump to end of comment
                if self.body.startswith("!--", i+1):
                    i += 4
                    while i < n and not self.body.startswith("-->", i):
                        i += 1
                    i += 3
                    continue
                
                # flush buffer contents before tag
                if text:
                    self.add_text(''.join(text))
                in_tag = True
                text = []
                
            elif c == ">" and in_tag and not in_attribute:
                in_tag = False
                tag = ''.join(text)
                self.add_tag(tag)
                text = []
                
                # jump to matching </script> tag, add text to tag
                if tag == "script":
                    end = i+1
                    while end < n and not self.body.startswith("</script>", end):
                        end += 1
                    script_text = self.body[i+1:end]
                    if script_text:
                        self.add_text(script_text)
                    self.add_tag('/script')
                    i = end + 8
                    
            # track enter or leaving quoted attribute
            elif in_tag and (c == '"' or c == "'"):
                if not in_attribute:
                    quote = c
                    in_attribute = True
                elif in_attribute and quote == c:
                    quote = None
                    in_attribute = False
                text.append(c) # preserve the quotes!
                
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
            if tag[1:] in FORMAT_TAGS:
                # mis-nested formatting tags, e.g. <u> hi <b></u> Bold <i> both </b> italic </i>
                # when encountering a closing formatting tag,
                # read from unfinished top to bottom into a list UNTIL a matching opening tag is found
                # the next time implicit_tags is called, place each tag in the list
                self.close_formatting(tag[1:])
            else:
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
        parts = text.split(None, 1)
        if len(parts) == 1:
            return parts[0], {}

        tag, rest = parts[0].casefold(), parts[1]
        attributes = {}
        n = len(rest)
        i = 0
        def skip_whitespace(i):
            while i < n and rest[i].isspace():
                i += 1
            return i
         
        while i < n:
            i = skip_whitespace(i)
            if i >= n:
                break
            
            # read attribute name up until space or =
            start = i
            while i < n and rest[i] not in "= ":
                i += 1
            attr_name = rest[start:i]
            i = skip_whitespace(i)
            
            # read value
            if i < n and rest[i] == "=":
                i = skip_whitespace(i+1)
                # quoted attribute, read until end quote
                if i < n and rest[i] in ("'", '"'):
                    quote = rest[i]
                    i += 1
                    start = i
                    while i < n and rest[i] != quote:
                        i += 1
                    attr_val = rest[start:i]
                    i += 1
                else:
                    start = i
                    while i < n and not rest[i].isspace():
                        i += 1
                    attr_val = rest[start:i]
            
            else:
                attr_val = ""

            attributes[attr_name.casefold()] = attr_val
        
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
            
    def close_formatting(self, tag):
        reopen = []
        
        # go backwards and finish any open format tags UNTIL we see a matching tag
        while True:
            top = self.unfinished[-1].tag            
            if top not in FORMAT_TAGS: return
            
            top = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(top)
            
            if top.tag == tag: break
            reopen.append(top.tag) # don't need to re-open the actual requested tag
        
        # reopen all of our tags, in reverse order
        while reopen:
            self.add_tag(reopen.pop())
            
def print_tree(node, source=False, indent=0): # source mode: print tag attributes and closing tags
    spacing = "    " * indent
    if isinstance(node, Text):
        return node.text
    
    if len(node.children) == 1 and isinstance(node.children[0], Text) and "\n" not in node.children[0].text:
        return f"{spacing}<{node.tag}>{node.children[0].text}</{node.tag}>"
    
    open = f"{spacing}<{node.tag}>"
    inner = []
    for child in node.children:
        if isinstance(child, Text) and node.tag != "pre":
            text = child.text.strip()
            if text:
                inner.append(f"{'    '*(indent+1)}{text}")
        else:
            inner.append(print_tree(child, source, indent+1))
    close = f"{spacing}</{node.tag}>"
    if source:
        return "\n".join([open] + inner + [close])
    return "\n".join([open] + inner)    

if __name__ == "__main__":
    from url import URL
    import sys
    url = "file:///home/yuzu/Documents/browser-dev/hi"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    body = URL(url).request()
    nodes = HTMLParser(body).parse()
    print(print_tree(nodes, source=True))