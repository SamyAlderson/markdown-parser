from bs4 import BeautifulSoup
from typing import Union

class MarkdownParser:
    """
    A Markdown parser that converts Markdown text into HTML.
    
    The parser handles common Markdown elements such as headings, bold text, 
    italics, and lists.
    
    :cvar headings_map: Map of heading levels to HTML tags
    :vartype headings_map: dict
    :cvar bold_text_pattern: Pattern for bold text
    :vartype bold_text_pattern: str
    :cvar italic_text_pattern: Pattern for italic text
    :vartype italic_text_pattern: str
    :cvar link_pattern: Pattern for links
    :vartype link_pattern: str
    :cvar unordered_list_pattern: Pattern for unordered lists
    :vartype unordered_list_pattern: str
    :cvar ordered_list_pattern: Pattern for ordered lists
    :vartype ordered_list_pattern: str
    """

    headings_map = {
        1: 'h1',
        2: 'h2',
        3: 'h3',
        4: 'h4',
        5: 'h5',
        6: 'h6',
    }

    bold_text_pattern = r'\*\*(.*?)\*\*'
    italic_text_pattern = r'\*(.*?)\*'
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    unordered_list_pattern = r'^\s*[-+*]\s+(.*)$'
    ordered_list_pattern = r'^\s*\d+\.\s+(.*)$'

    def __init__(self):
        """
        Initializes the Markdown parser.
        """

    def _parse_heading(self, heading: str, level: int) -> BeautifulSoup:
        """
        Parses a heading and returns it as a BeautifulSoup tag.
        
        :param heading: The heading text
        :param level: The heading level
        :return: The parsed heading as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        tag = BeautifulSoup(f'<{self.headings_map[level]}>{heading}</{self.headings_map[level]}>', 'html.parser')
        return tag

    def _parse_bold_text(self, text: str) -> BeautifulSoup:
        """
        Parses bold text and returns it as a BeautifulSoup tag.
        
        :param text: The bold text
        :return: The parsed bold text as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        tag = BeautifulSoup(f'<b>{text}</b>', 'html.parser')
        return tag

    def _parse_italic_text(self, text: str) -> BeautifulSoup:
        """
        Parses italic text and returns it as a BeautifulSoup tag.
        
        :param text: The italic text
        :return: The parsed italic text as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        tag = BeautifulSoup(f'<i>{text}</i>', 'html.parser')
        return tag

    def _parse_link(self, link: str) -> BeautifulSoup:
        """
        Parses a link and returns it as a BeautifulSoup tag.
        
        :param link: The link text and URL
        :return: The parsed link as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        text, url = self._parse_link_text_and_url(link)
        tag = BeautifulSoup(f'<a href="{url}">{text}</a>', 'html.parser')
        return tag

    def _parse_link_text_and_url(self, link: str) -> tuple:
        """
        Parses a link and returns the text and URL as a tuple.
        
        :param link: The link text and URL
        :return: The link text and URL as a tuple
        :rtype: tuple
        """
        match = self.link_pattern.match(link)
        if not match:
            raise ValueError('Invalid link format')
        return match.group(1), match.group(2)

    def _parse_unordered_list_item(self, item: str) -> BeautifulSoup:
        """
        Parses an unordered list item and returns it as a BeautifulSoup tag.
        
        :param item: The list item text
        :return: The parsed list item as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        tag = BeautifulSoup(f'<li>{item}</li>', 'html.parser')
        return tag

    def _parse_ordered_list_item(self, item: str, index: int) -> BeautifulSoup:
        """
        Parses an ordered list item and returns it as a BeautifulSoup tag.
        
        :param item: The list item text
        :param index: The list item index
        :return: The parsed list item as a BeautifulSoup tag
        :rtype: bs4.element.Tag
        """
        tag = BeautifulSoup(f'<li>{index}. {item}</li>', 'html.parser')
        return tag

    def parse(self, markdown_text: str) -> BeautifulSoup:
        """
        Parses Markdown text into HTML.
        
        :param markdown_text: The Markdown text to parse
        :return: The parsed HTML as a BeautifulSoup tag
        :rtype: bs4.element.Document
        """
        soup = BeautifulSoup(markdown_text, 'html.parser')

        # Parse headings
        for heading in soup.find_all('h1', 'h6'):
            level = int(heading.name[1])  # Get the heading level from the tag name
            text = heading.text
            soup.replace(heading, self._parse_heading(text, level))

        # Parse bold text
        for tag in soup.find_all(text=self.bold_text_pattern):
            tag.replace_with(self._parse_bold_text(tag.extract().group(1)))

        # Parse italic text
        for tag in soup.find_all(text=self.italic_text_pattern):
            tag.replace_with(self._parse_italic_text(tag.extract().group(1)))

        # Parse links
        for tag in soup.find_all(text=self.link_pattern):
            tag.replace_with(self._parse_link(tag.extract().group(0)))

        # Parse unordered lists
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li'):
                text = li.text
                soup.replace(li, self._parse_unordered_list_item(text))

        # Parse ordered lists
        for ol in soup.find_all('ol'):
            for li in ol.find_all('li'):
                index = len(ol.find_all('li')) - 1 - list(ol.find_all('li')).index(li)
                text = li.text
                soup.replace(li, self._parse_ordered_list_item(text, index))

        return soup

def main():
    parser = MarkdownParser()
    markdown_text = '# Heading 1\n## Heading 2\n### Heading 3\n\nBold text: **bold text**\nItalic text: *italic text*\n\n[Link text](http://www.example.com)\n\n- List item 1\n- List item 2\n\n1. Ordered list item 1\n2. Ordered list item 2'
    html = parser.parse(markdown_text)
    print(html.prettify())

if __name__ == '__main__':
    main()
```

Please note that this code assumes that the `beautifulsoup4` and `lxml` libraries are installed. You can install them using pip:

```bash
pip install beautifulsoup4 lxml