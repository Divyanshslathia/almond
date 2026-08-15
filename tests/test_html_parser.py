"""
Tests for HTML parser.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.html_parser import (
    HTMLTokenizer, HTMLParser, parse_html,
    HTMLElement, HTMLText
)


class TestHTMLTokenizer(unittest.TestCase):
    """Test HTML tokenization."""

    def test_simple_tag(self):
        """Test tokenizing a simple tag."""
        tokenizer = HTMLTokenizer("<p>Hello</p>")
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, 'TAG_OPEN')
        self.assertEqual(tokens[0].data['tag'], 'p')
        self.assertEqual(tokens[1].type, 'TEXT')
        self.assertEqual(tokens[1].data, 'Hello')
        self.assertEqual(tokens[2].type, 'TAG_CLOSE')

    def test_nested_tags(self):
        """Test nested tags."""
        tokenizer = HTMLTokenizer("<div><p>Hello</p></div>")
        tokens = tokenizer.tokenize()

        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].data['tag'], 'div')
        self.assertEqual(tokens[1].data['tag'], 'p')
        self.assertEqual(tokens[2].data, 'Hello')

    def test_attributes(self):
        """Test parsing attributes."""
        tokenizer = HTMLTokenizer('<a href="http://example.com">Link</a>')
        tokens = tokenizer.tokenize()

        self.assertEqual(tokens[0].data['attrs']['href'], 'http://example.com')

    def test_self_closing_tag(self):
        """Test self-closing tags."""
        tokenizer = HTMLTokenizer('<br />')
        tokens = tokenizer.tokenize()

        self.assertEqual(tokens[0].type, 'TAG_SELF_CLOSE')
        self.assertEqual(tokens[0].data['tag'], 'br')


class TestHTMLParser(unittest.TestCase):
    """Test HTML parsing."""

    def test_simple_html(self):
        """Test parsing simple HTML."""
        root = parse_html("<html><body><h1>Hello</h1></body></html>")

        self.assertEqual(root.tag, 'document')
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].tag, 'html')

    def test_text_content(self):
        """Test text content extraction."""
        root = parse_html("<p>Hello World</p>")

        p_element = root.children[0]
        self.assertEqual(p_element.tag, 'p')
        self.assertEqual(len(p_element.children), 1)
        self.assertIsInstance(p_element.children[0], HTMLText)
        self.assertEqual(p_element.children[0].text, 'Hello World')

    def test_nested_structure(self):
        """Test nested HTML structure."""
        root = parse_html("<div><p>Text</p><p>More</p></div>")

        div = root.children[0]
        self.assertEqual(div.tag, 'div')
        self.assertEqual(len(div.children), 2)
        self.assertEqual(div.children[0].tag, 'p')
        self.assertEqual(div.children[1].tag, 'p')

    def test_attributes(self):
        """Test attribute parsing."""
        root = parse_html('<a href="http://example.com" class="link">Click</a>')

        a_element = root.children[0]
        self.assertEqual(a_element.attrs['href'], 'http://example.com')
        self.assertEqual(a_element.attrs['class'], 'link')

    def test_real_html_example(self):
        """Test parsing real HTML example."""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Welcome</h1>
                <p>This is a <strong>test</strong> page.</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </body>
        </html>
        """

        root = parse_html(html)

        # Should have html element
        self.assertEqual(root.children[0].tag, 'html')

        # HTML should have head and body
        html_elem = root.children[0]
        self.assertEqual(len(html_elem.children), 2)
        self.assertEqual(html_elem.children[0].tag, 'head')
        self.assertEqual(html_elem.children[1].tag, 'body')


if __name__ == '__main__':
    unittest.main()
