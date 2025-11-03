import socket
import ssl
import gzip

class URL:
    def __init__(self, url: str):
        self.redirects = 0
        self.s = None # socket placeholder
        self._init_state(url)
    
    def _init_state(self, url: str) -> None:
        """Extracts parts of URL
        - **scheme** - data: OR (view-source):[http, https, file]
        - data accepts **chartype** [US-ASCII, UTF-8] and **MIME-TYPE** [text/plain, text/html]"""
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
            
        self.source = False
        
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

    def request(self, headers: dict={}) -> str:
        """Performs a **GET** request using HTTP/1.1 connection: keep-alive
        \n Automatically performs up to 100 redirects"""
        content = ""
        if self.scheme == "file":
            try:
                with open(self.path, 'r') as file:
                    content = file.read()
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
        
        else:
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
            else:
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
                
                elif "content-length" in response_headers:
                    content = response.read(int(response_headers["content-length"]))
                    
                # decompress and decode 
                if response_headers.get("content-encoding") == "gzip":
                    content = gzip.decompress(content).decode("utf-8")
                else:
                    content = content.decode("utf-8")
                
            self.redirects = 0
        
        if self.source:
            return content.replace("<", "&lt;").replace(">", "&gt;")
        return content
    
    def _redirect(self, location: str) -> str:
        if self.redirects >= 100:
            return "Error: Redirect Limit Reached"

        if location.startswith("/"):
            self.path = location
        else:
            self._init_state(location)
        
        self.redirects += 1
        return self.request()
    
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
            
def load(url: str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Encoding": "gzip"
    }
    show(url.request(headers))
    
if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "file:///home/yuzu/Documents/browser-dev/hi"
    load(URL(url))
    
        