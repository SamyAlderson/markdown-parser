# src/main.py

"""
Main entry point for the Markdown parser.

This module provides a command-line interface to the Markdown parser.
"""

import argparse
from typing import Dict
from markdown_parser import MarkdownParser

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Markdown parser")
    parser.add_argument("-i", "--input", help="Path to Markdown input file", required=True)
    parser.add_argument("-o", "--output", help="Path to output HTML file", required=True)
    return parser.parse_args()

def main() -> None:
    """
    Main entry point for the Markdown parser.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    args = parse_args()

    try:
        markdown_parser = MarkdownParser()
        with open(args.input, "r") as f:
            markdown_text = f.read()
            html = markdown_parser.parse(markdown_text)
            with open(args.output, "w") as f:
                f.write(html)
        print(f"Successfully parsed Markdown and wrote output to {args.output}")
    except FileNotFoundError as e:
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
```

```python
# src/markdown_parser.py

"""
Implementation of the Markdown parser.
"""

import re
from typing import Dict, List
from bs4 import BeautifulSoup, Tag

class MarkdownParser:
    """
    Markdown parser.

    Provides methods for parsing Markdown text into HTML.
    """

    def parse(self, markdown_text: str) -> str:
        """
        Parse Markdown text into HTML.

        Args:
            markdown_text (str): Markdown text to parse.

        Returns:
            str: Parsed HTML.
        """
        # Parse headings
        headings: Dict[str, List[Tag]] = self._parse_headings(markdown_text)
        # Parse bold and italic text
        bold_italic_text: str = self._parse_bold_italic(markdown_text)
        # Parse lists
        lists: List[Tag] = self._parse_lists(markdown_text)
        # Parse links
        links: List[Tag] = self._parse_links(markdown_text)
        # Create HTML soup
        html = BeautifulSoup(markdown_text, "lxml")
        # Add parsed elements to HTML soup
        html.append(self._add_headings(headings))
        html.append(self._add_bold_italic_text(bold_italic_text))
        html.append(self._add_lists(lists))
        html.append(self._add_links(links))
        # Return parsed HTML
        return str(html)

    def _parse_headings(self, markdown_text: str) -> Dict[str, List[Tag]]:
        """
        Parse Markdown headings.

        Args:
            markdown_text (str): Markdown text to parse.

        Returns:
            Dict[str, List[Tag]]: Parsed headings.
        """
        headings: Dict[str, List[Tag]] = {}
        for match in re.finditer(r"^(#{1,6}) (.*)$", markdown_text, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2)
            heading = Tag(name="h" + str(level), text=text)
            if level not in headings:
                headings[level] = []
            headings[level].append(heading)
        return headings

    def _parse_bold_italic(self, markdown_text: str) -> str:
        """
        Parse Markdown bold and italic text.

        Args:
            markdown_text (str): Markdown text to parse.

        Returns:
            str: Parsed bold and italic text.
        """
        bold_italic_text = markdown_text
        bold_italic_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", bold_italic_text)
        bold_italic_text = re.sub(r"__(.*?)__", r"<i>\1</i>", bold_italic_text)
        return bold_italic_text

    def _parse_lists(self, markdown_text: str) -> List[Tag]:
        """
        Parse Markdown lists.

        Args:
            markdown_text (str): Markdown text to parse.

        Returns:
            List[Tag]: Parsed lists.
        """
        lists: List[Tag] = []
        for match in re.finditer(r"^(\s*- )(.*)$", markdown_text, re.MULTILINE):
            text = match.group(2)
            item = Tag(name="li", text=text)
            lists.append(item)
        return lists

    def _parse_links(self, markdown_text: str) -> List[Tag]:
        """
        Parse Markdown links.

        Args:
            markdown_text (str): Markdown text to parse.

        Returns:
            List[Tag]: Parsed links.
        """
        links: List[Tag] = []
        for match in re.finditer(r"\[(.*?)\]\((.*?)\)", markdown_text):
            text = match.group(1)
            url = match.group(2)
            link = Tag(name="a", text=text, attrs={"href": url})
            links.append(link)
        return links

    def _add_headings(self, headings: Dict[str, List[Tag]]) -> Tag:
        """
        Add parsed headings to HTML soup.

        Args:
            headings (Dict[str, List[Tag]]): Parsed headings.

        Returns:
            Tag: Added headings.
        """
        heading: Tag = Tag(name="h1")
        for level, items in headings.items():
            for item in items:
                heading.append(item)
        return heading

    def _add_bold_italic_text(self, text: str) -> Tag:
        """
        Add parsed bold and italic text to HTML soup.

        Args:
            text (str): Parsed bold and italic text.

        Returns:
            Tag: Added bold and italic text.
        """
        return Tag(name="p", text=text)

    def _add_lists(self, lists: List[Tag]) -> Tag:
        """
        Add parsed lists to HTML soup.

        Args:
            lists (List[Tag]): Parsed lists.

        Returns:
            Tag: Added lists.
        """
        list_element = Tag(name="ul")
        for item in lists:
            list_element.append(item)
        return list_element

    def _add_links(self, links: List[Tag]) -> Tag:
        """
        Add parsed links to HTML soup.

        Args:
            links (List[Tag]): Parsed links.

        Returns:
            Tag: Added links.
        """
        list_element = Tag(name="ul")
        for link in links:
            list_element.append(link)
        return list_element
```

```python
# tests/test_markdown_parser.py

"""
Unit tests for the Markdown parser.
"""

import unittest
from markdown_parser import MarkdownParser

class TestMarkdownParser(unittest.TestCase):
    def test_parse_headings(self):
        markdown_text = """# Heading 1
## Heading 2
### Heading 3"""
        parser = MarkdownParser()
        headings = parser._parse_headings(markdown_text)
        self.assertEqual(headings, {1: [Tag(name="h1", text="Heading 1")], 2: [Tag(name="h2", text="Heading 2")], 3: [Tag(name="h3", text="Heading 3")]})

    def test_parse_bold_italic(self):
        markdown_text = """**Bold text** _Italic text_"""
        parser = MarkdownParser()
        bold_italic_text = parser._parse_bold_italic(markdown_text)
        self.assertEqual(bold_italic_text, "<b>Bold text</b> <i>Italic text</i>")

    def test_parse_lists(self):
        markdown_text = """- Item 1
- Item 2"""
        parser = MarkdownParser()
        lists = parser._parse_lists(markdown_text)
        self.assertEqual(lists, [Tag(name="li", text="Item 1"), Tag(name="li", text="Item 2")])

    def test_parse_links(self):
        markdown_text = """[Link text](https://www.example.com)"""
        parser = MarkdownParser()
        links = parser._parse_links(markdown_text)
        self.assertEqual(links, [Tag(name="a", text="Link text", attrs={"href": "https://www.example.com"})])

if __name__ == "__main__":
    unittest.main()