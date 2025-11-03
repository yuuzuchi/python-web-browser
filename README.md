# Simple Python Web Browser

A small web browser implemented in a single Python script (`main.py`).  
Demonstrates low-level HTTP(S) requests using sockets and basic HTML text extraction (prints text between tags).

## What it does
- Performs simple HTTP/HTTPS GET requests (HTTP/1.1).
- Supports `file://` and `data:` URLs.
- Supports `view-source:` prefix to show HTML source with angle brackets escaped.
- Prints only the text content between HTML tags.
- Automatically follows redirects.

## Requirements
- Python 3.7+ (f-strings and ssl.create_default_context).
- Network access for HTTP/HTTPS.

## How to run
From the repository root (where `main.py` is located), run:

```bash
# Fetch a website over HTTP
python3 main.py "http://example.org/"

# Fetch a website over HTTPS
python3 main.py "https://example.org/"

# Open a local file (absolute path expected after file://)
python3 main.py "file:///home/you/path/to/file.html"

# data URI (plain text)
python3 main.py "data:text/plain,Hello%20world"

# data URI (base64)
python3 main.py "data:text/plain;base64,SGVsbG8gV29ybGQh"

# View the source (angle brackets escaped)
python3 main.py "view-source:http://example.org/"
```