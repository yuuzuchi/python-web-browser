import socket
import ssl
import gzip

def is_url(url: str):
    if " " in url:
        return False
    if url.startswith("about:blank") or url.startswith("data:"):
        return True
    if "://" in url and all(url.split("://")):
        return True

class URL:
    def __init__(self, url: str):
        self.redirects = 0
        self.s = None # socket placeholder
        self._init_state(url)
    
    def __str__(self):
        try:
            if self.scheme == "data":
                return self.url_str
            
            port_part = ":" + str(self.port)
            if self.scheme == "https" and self.port == 443:
                port_part = ""
            if self.scheme == "http" and self.port == 80:
                port_part = ""
            return f"{self.scheme}://{self.host}{port_part}{self.path}{"#" + self.fragment if self.fragment else ""}"
        except Exception:
            return "about:blank"
        
    def __repr__(self): return self.__str__()
    
    def _init_state(self, url: str) -> None:
        self.url_str = url
        """Extracts parts of URL
        - **scheme** - data: OR (view-source):[http, https, file]
        - data accepts **chartype** [US-ASCII, UTF-8] and **MIME-TYPE** [text/plain, text/html]"""
        if url == "about:blank":
            self.scheme = "blank"
            return 
        
        try:
            if url.startswith("data:"):
                self.scheme = "data"
                meta, self.data = url[5:].split(",", 1)
                self.charset='US-ASCII'
                self.base64 = False
                
                parts = meta.split(";")
                self.mime = parts[0] or "text/plain"
                
                for part in parts[1:]:
                    if part.startswith("charset="):
                        self.charset = part.split("=", 1)[1]
                    elif part == "base64":
                        self.base64 = True

                assert self.mime in ("text/plain", "text/html")
                assert self.charset in ("US-ASCII", "UTF-8")
                return
        except Exception:
            print("URL data error!")
            self._init_state("about:blank")
            
        self.source = False
        
        # if no scheme provided (like google.com), auto prefix with https
        if "://" not in url:
            self.url_str = url = "https://" + url
        
        try:
            self.scheme, url = url.split("://", 1)
            if self.scheme.startswith("view-source:"):
                self.source = True
                self.scheme = self.scheme.split(":", 1)[1]
            assert self.scheme in ["http", "https", "file"]
            
            if "/" not in url:
                url += "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            self.port = 80 if self.scheme == "http" else 443
            
            # custom ports
            if ":" in self.host:
                self.host, self.port = self.host.split(":",1)
                self.port = int(self.port)
                
            self.path, sep, fragment = self.path.partition("#")
            self.fragment = None
            if sep:
                self.fragment = fragment
                
            # close socket if host/port changed
            if self.s is not None:
                print("closed")
                self.s.close()
                self.s = None
        except Exception:
            print("URL scheme error!")
            self._init_state("about:blank")

    def request(self, headers: dict={}) -> str:
        print("request:", self.url_str)
        """Performs a **GET** request using HTTP/1.1 connection: keep-alive
        \n Automatically performs up to 100 redirects"""
        if self.scheme == "blank":
            return ""
        
        if self.scheme == "file":
            try:
                with open(self.path, 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return f"Error: The file '{self.path}' was not found."
            except Exception as e:
                return f"Error: {e}"
            
        elif self.scheme == "data":
            if self.base64:
                import base64
                base64b = base64.b64decode(self.data)
                return base64b.decode("utf8" if self.charset.lower() == "UTF-8" else "ascii")
            return self.data
        
        # http and https
        if not self.s:
            self.s = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP
            ) 
            if self.scheme == "https":
                ctx = ssl.create_default_context()
                self.s = ctx.wrap_socket(self.s, server_hostname=self.host)
                
            self.s.connect((self.host, self.port))

        request =  f"GET {self.path} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        request += f"Connection: keep-alive\r\n"
        for header, value in headers.items():
            request += f"{header}: {value}\r\n"
        request += "\r\n"

        self.s.send(request.encode("utf8"))
        response = self.s.makefile("rb", encoding="utf8", newline="\r\n")
        statusline = response.readline().decode("utf-8")
        print("Statusline:", statusline.strip())
        version, status, explanation = statusline.split(" ", 2)
        
        response_headers = {}
        while True:
            line = response.readline().decode("utf-8")
            if line == "\r\n": 
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        
        # handle redirects
        if status.startswith('3') and "location" in response_headers:
            content = self._redirect(response_headers["location"])
            self.redirects = 0
            return content
        
        # unchunk the data
        content = bytearray()
        if response_headers.get("transfer-encoding") == "chunked":
            while True:
                chunk_size = int(response.readline().decode("utf-8").strip(), 16)
                if chunk_size == 0:
                    break
                chunk = response.read(chunk_size)
                content.extend(chunk)
                response.read(2)
        
        # content-length cannot appear if chunked
        elif "content-length" in response_headers:
            content = response.read(int(response_headers["content-length"]))
            
        # decompress and decode 
        if response_headers.get("content-encoding") == "gzip":
            content = gzip.decompress(content)
            
        return content.decode("utf-8")
                
    def _redirect(self, location: str) -> str:
        print("Redirecting to", location)
        if self.redirects >= 100:
            return "Error: Redirect Limit Reached"

        if location.startswith("/"):
            self.path = location
        else:
            self._init_state(location)
        
        self.redirects += 1
        return self.request()

    def resolve(self, url: str, from_user_input: bool = False):
        if url.startswith("#"): # fragment link, return URL with no_load_required flag
            new_url = URL(str(self))
            new_url.fragment = url[1:]
            new_url.fragment_no_load_required = True
            return new_url

        # if fragment is at end of link, remove and add back after resolving
        url, frag_sep, frag = url.partition("#")
        base, sep, query = url.partition("?")
        resolved = self.resolve_path_and_host(base, from_user_input)

        if sep:
            return URL(f"{resolved}?{query}{"#" + frag if frag_sep else ""}")
        return URL(f"{resolved}{"#" + frag if frag_sep else ""}")
                          
    def resolve_path_and_host(self, base, from_user_input):
        # is full scheme: return as is
        if "://" in base: return base

        if not base.startswith("/"):
            # user typed shortened URL (e.g. "google.com") in address bar
            if from_user_input: 
                if "." in base and " " not in base:
                    return f"https://{base}"
                else:
                    return f"http://frogfind.com/?q={base}"
                
            dir, _ = self.path.rsplit("/", 1)
            while base.startswith("../"):
                _, base = base.split("/", 1)
                if "/" in dir:
                    dir, _ = dir.rsplit("/", 1)
            base = dir + "/" + base
            
        # //host/path
        if base.startswith("//"):
            return f"{self.scheme}:{base}"

        # absolute path starting with /
        else:
            return f"{self.scheme}://{self.host}:{str(self.port)}{base}"
            
        
    
def show(body: str) -> None: # print all text between tags
    in_tag = False
    i = 0
    while i < len(body):
        c = body[i]
        if c == "<": in_tag = True
        elif c == ">": in_tag = False
        elif not in_tag:
            if c == "&":
                if body[i+1:i+4] == "lt;":
                    c = "<"
                elif body[i+1:i+4] == "gt;":
                    c = ">"
                i += 3
            print(c, end='')
        i += 1
            
def load(url: URL) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Encoding": "gzip"
    }
    if url.source:
        print(url.request(headers))
    else:
        show(url.request(headers))
    
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "file:///home/yuzu/Documents/browser-dev/hi"
    load(URL(url))
    
        