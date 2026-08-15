"""
Tests for DOM tree.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.html_parser import parse_html
from browser.dom import build_dom, DOMDocument, DOMElement, DOMText


class TestDOM(unittest.TestCase):
    """Test DOM tree construction."""

    def test_build_simple_dom(self):
        """Test building a simple DOM."""
        html = "<html><body><p>Hello</p></body></html>"
        html_root = parse_html(html)
        dom = build_dom(html_root)

        self.assertIsInstance(dom, DOMDocument)
        self.assertEqual(len(dom.children), 1)
        self.assertIsInstance(dom.children[0], DOMElement)
        self.assertEqual(dom.children[0].tag_name, 'html')

    def test_dom_text_nodes(self):
        """Test that text nodes are preserved."""
        html = "<p>Hello World</p>"
        html_root = parse_html(html)
        dom = build_dom(html_root)

        p_element = dom.children[0]
        self.assertEqual(p_element.tag_name, 'p')
        self.assertEqual(len(p_element.children), 1)
        self.assertIsInstance(p_element.children[0], DOMText)
        self.assertEqual(p_element.children[0].text, 'Hello World')

    def test_dom_attributes(self):
        """Test that attributes are preserved."""
        html = '<a href="http://example.com" class="link">Click</a>'
        html_root = parse_html(html)
        dom = build_dom(html_root)

        a_element = dom.children[0]
        self.assertEqual(a_element.get_attribute('href'), 'http://example.com')
        self.assertEqual(a_element.get_attribute('class'), 'link')

    def test_nested_dom_structure(self):
        """Test nested DOM structure."""
        html = """
        <html>
            <body>
                <div>
                    <h1>Title</h1>
                    <p>Paragraph</p>
                </div>
            </body>
        </html>
        """
        html_root = parse_html(html)
        dom = build_dom(html_root)

        # Navigate down the tree
        html_elem = dom.children[0]
        self.assertEqual(html_elem.tag_name, 'html')

        body_elem = html_elem.children[0]
        self.assertEqual(body_elem.tag_name, 'body')

        div_elem = body_elem.children[0]
        self.assertEqual(div_elem.tag_name, 'div')

        self.assertEqual(len(div_elem.children), 2)
        self.assertEqual(div_elem.children[0].tag_name, 'h1')
        self.assertEqual(div_elem.children[1].tag_name, 'p')

    def test_parent_child_relationships(self):
        """Test that parent-child relationships are set correctly."""
        html = "<div><p>Test</p></div>"
        html_root = parse_html(html)
        dom = build_dom(html_root)

        div = dom.children[0]
        p = div.children[0]

        # Check parent relationships
        self.assertEqual(p.parent, div)
        self.assertEqual(div.parent, dom)


if __name__ == '__main__':
    unittest.main()
