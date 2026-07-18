import unittest
from unittest.mock import patch
from markdown_parser import MarkdownParser
from bs4 import BeautifulSoup

class TestMarkdownParser(unittest.TestCase):

    def test_parse_headings(self):
        parser = MarkdownParser()
        markdown_text = "# Heading 1\n## Heading 2\n### Heading 3"
        expected_html = "<h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    def test_parse_bold_text(self):
        parser = MarkdownParser()
        markdown_text = "**Bold text**"
        expected_html = "<b>Bold text</b>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    def test_parse_italic_text(self):
        parser = MarkdownParser()
        markdown_text = "*Italic text*"
        expected_html = "<i>Italic text</i>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    def test_parse_lists(self):
        parser = MarkdownParser()
        markdown_text = "- Item 1\n- Item 2\n1. Item 3\n2. Item 4"
        expected_html = "<ul><li>Item 1</li><li>Item 2</li></ul><ol><li>Item 3</li><li>Item 4</li></ol>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    def test_parse_links(self):
        parser = MarkdownParser()
        markdown_text = "[Link](https://www.example.com)"
        expected_html = "<a href='https://www.example.com'>Link</a>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    def test_parse_multiple_elements(self):
        parser = MarkdownParser()
        markdown_text = "# Heading 1\n**Bold text**\n*Italic text*"
        expected_html = "<h1>Heading 1</h1><b>Bold text</b><i>Italic text</i>"
        self.assertEqual(parser.parse(markdown_text), expected_html)

    @patch('markdown_parser.BeautifulSoup')
    def test_parse_invalid_markdown(self, mock_beautiful_soup):
        parser = MarkdownParser()
        markdown_text = "Invalid markdown"
        expected_html = ""
        mock_beautiful_soup.from_string.return_value = ""
        self.assertEqual(parser.parse(markdown_text), expected_html)

    @patch('markdown_parser.BeautifulSoup')
    def test_parse_empty_markdown(self, mock_beautiful_soup):
        parser = MarkdownParser()
        markdown_text = ""
        expected_html = ""
        mock_beautiful_soup.from_string.return_value = ""
        self.assertEqual(parser.parse(markdown_text), expected_html)

if __name__ == '__main__':
    unittest.main()