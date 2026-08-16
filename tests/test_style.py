"""
Tests for style calculation.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.style import calculate_styles, DEFAULT_STYLES
from browser.css_parser import CSSRule
from browser.dom import DOMElement, DOMText, DOMDocument


def test_default_styles():
    """Test that default styles are applied."""
    root = DOMDocument()
    p = DOMElement("p")
    root.add_child(p)

    calculate_styles(root, [])

    assert hasattr(p, 'styles')
    assert p.styles['display'] == 'block'
    assert p.styles['margin'] == '10px 0'


def test_css_rule_overrides_default():
    """Test that CSS rules override default styles."""
    root = DOMDocument()
    p = DOMElement("p")
    root.add_child(p)

    rules = [CSSRule("p", {"color": "red", "margin": "20px"})]
    calculate_styles(root, rules)

    assert p.styles['color'] == 'red'
    assert p.styles['margin'] == '20px'  # Overrides default
    assert p.styles['display'] == 'block'  # Still has default


def test_class_selector_styles():
    """Test that class selectors apply styles."""
    root = DOMDocument()
    p = DOMElement("p", {"class": "warning"})
    root.add_child(p)

    rules = [CSSRule(".warning", {"color": "orange"})]
    calculate_styles(root, rules)

    assert p.styles['color'] == 'orange'


def test_id_selector_styles():
    """Test that ID selectors apply styles."""
    root = DOMDocument()
    div = DOMElement("div", {"id": "header"})
    root.add_child(div)

    rules = [CSSRule("#header", {"background": "gray"})]
    calculate_styles(root, rules)

    assert div.styles['background'] == 'gray'


def test_multiple_matching_rules():
    """Test that multiple matching rules are applied."""
    root = DOMDocument()
    p = DOMElement("p", {"class": "warning"})
    root.add_child(p)

    rules = [
        CSSRule("p", {"margin": "5px"}),
        CSSRule(".warning", {"color": "orange"})
    ]
    calculate_styles(root, rules)

    assert p.styles['margin'] == '5px'
    assert p.styles['color'] == 'orange'


def test_nested_elements_get_styles():
    """Test that nested elements receive styles."""
    root = DOMDocument()
    div = DOMElement("div")
    p = DOMElement("p")
    div.add_child(p)
    root.add_child(div)

    rules = [CSSRule("p", {"color": "blue"})]
    calculate_styles(root, rules)

    assert p.styles['color'] == 'blue'


def test_text_nodes_unaffected():
    """Test that text nodes don't get styles."""
    root = DOMDocument()
    text = DOMText("Hello")
    root.add_child(text)

    rules = []
    calculate_styles(root, rules)

    # Text nodes shouldn't have styles attribute
    assert not hasattr(text, 'styles')


def test_heading_default_styles():
    """Test that headings get proper default styles."""
    root = DOMDocument()
    h1 = DOMElement("h1")
    h2 = DOMElement("h2")
    h3 = DOMElement("h3")
    root.add_child(h1)
    root.add_child(h2)
    root.add_child(h3)

    calculate_styles(root, [])

    assert h1.styles['font-size'] == '32px'
    assert h2.styles['font-size'] == '24px'
    assert h3.styles['font-size'] == '18px'
    assert h1.styles['font-weight'] == 'bold'


def test_link_default_styles():
    """Test that links get proper default styles."""
    root = DOMDocument()
    a = DOMElement("a")
    root.add_child(a)

    calculate_styles(root, [])

    assert a.styles['color'] == 'blue'
    assert a.styles['text-decoration'] == 'underline'


if __name__ == "__main__":
    test_default_styles()
    test_css_rule_overrides_default()
    test_class_selector_styles()
    test_id_selector_styles()
    test_multiple_matching_rules()
    test_nested_elements_get_styles()
    test_text_nodes_unaffected()
    test_heading_default_styles()
    test_link_default_styles()
    print("All style calculation tests passed!")
