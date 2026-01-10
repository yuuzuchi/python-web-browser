# Simple Python Web Browser

Simple HTTP(S) browser using Python/TKinter, created with the guidance of the amazing [Web Browser Engineering](https://browser.engineering/) textbook! Sports custom HTML and CSS parsers, the latter of which is designed (mostly) in accordance to the csswg spec. No JS or dynamic page updates supported yet (WIP)

Extremely slow to style and layout websites, you have been warned!

## What it does
- Performs simple HTTP/HTTPS GET requests (HTTP/1.1).
- Additionally supports `file://` and `data:` URLs.
- Supports chunking and gzip compression.
- Automatically follows redirects.
- Parses the majority of HTML features (including `<style>`, `<script>`, `<!--comments-->`, etc).
- Tokenizes and parses CSS style rules, and matches with a selector engine.
- Layouts and renders a scrollable site with TKinter.
- Allows navigation with a URL bar, back/forward buttons, and clickable links. 

## Requirements
- Python 3.10+
- Network access for HTTP/HTTPS.

## How to run
From the repository root (where `browser.py` is located), run:

```bash
# Fetch a website over HTTP
python3 browser.py "http://example.org/"

# Fetch a website over HTTPS
python3 browser.py "https://example.org/"

# Open a local file (absolute path expected after file://)
python3 browser.py "file:///home/you/path/to/file.html"

# data URI (plain text)
python3 browser.py "data:text/plain,Hello%20world"

# data URI (base64)
python3 browser.py "data:text/plain;base64,SGVsbG8gV29ybGQh"

# View the source (angle brackets escaped)
python3 browser.py "view-source:http://example.org/"
```

To run individual files in modules (e.g. css/selector_matcher.py), run:

```bash
python3 -m css.selector_matcher
```