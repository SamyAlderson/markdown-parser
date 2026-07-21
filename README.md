# markdown-parser

A simple Markdown parser for Python

This utility takes Markdown text as input and outputs HTML. It supports common elements like headings, bold text, italics, and lists.

## What it does

I needed a quick way to convert Markdown text to HTML, so I wrote this parser. It's a single-purpose tool that gets the job done.

## Install

You can install it using pip:
```bash
pip install markdown-parser
```

## Usage

To use the parser, call the `parse` function with your Markdown text as an argument:
```python
from markdown_parser import parse

markdown_text = "# Heading\n## Subheading\nThis is a paragraph."
html = parse(markdown_text)
print(html)
```

## Build from Source

To build from source, clone the repository and run:
```bash
python setup.py install
```

## Run Tests

The parser has a test suite. You can run it using:
```bash
python -m unittest discover
```

## Project Structure

* `markdown_parser.py`: The main parser function
* `test_markdown_parser.py`: The test suite
* `setup.py`: The build script

## License

Copyright (c) 2026 SamyAlderson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.