"""
Tests for CSS parser.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.css_parser import parse_css, CSSRule, selector_matches
from browser.dom import DOMElement, DOMText


def test_parse_simple_rule():
    """Test parsing a simple CSS rule."""
    css = "p { color: blue; }"
    rules = parse_css(css)

    assert len(rules) == 1
    assert rules[0].selector == "p"
    assert rules[0].declarations["color"] == "blue"


def test_parse_multiple_declarations():
    """Test parsing a rule with multiple declarations."""
    css = "div { color: red; margin: 10px; padding: 5px; }"
    rules = parse_css(css)

    assert len(rules) == 1
    assert rules[0].selector == "div"
    assert rules[0].declarations["color"] == "red"
    assert rules[0].declarations["margin"] == "10px"
    assert rules[0].declarations["padding"] == "5px"


def test_parse_multiple_rules():
    """Test parsing multiple CSS rules."""
    css = """
    p { color: blue; }
    h1 { font-size: 24px; }
    div { margin: 0; }
    """
    rules = parse_css(css)

    assert len(rules) == 3
    assert rules[0].selector == "p"
    assert rules[1].selector == "h1"
    assert rules[2].selector == "div"


def test_parse_class_selector():
    """Test parsing class selector."""
    css = ".warning { color: orange; }"
    rules = parse_css(css)

    assert len(rules) == 1
    assert rules[0].selector == ".warning"
    assert rules[0].declarations["color"] == "orange"


def test_parse_id_selector():
    """Test parsing ID selector."""
    css = "#header { background: gray; }"
    rules = parse_css(css)

    assert len(rules) == 1
    assert rules[0].selector == "#header"
    assert rules[0].declarations["background"] == "gray"


def test_selector_matches_element():
    """Test element selector matching."""
    element = DOMElement("p")

    assert selector_matches("p", element) == True
    assert selector_matches("div", element) == False
    assert selector_matches("h1", element) == False


def test_selector_matches_class():
    """Test class selector matching."""
    element = DOMElement("p", {"class": "warning alert"})

    assert selector_matches(".warning", element) == True
    assert selector_matches(".alert", element) == True
    assert selector_matches(".error", element) == False


def test_selector_matches_id():
    """Test ID selector matching."""
    element = DOMElement("div", {"id": "header"})

    assert selector_matches("#header", element) == True
    assert selector_matches("#footer", element) == False


def test_parse_empty_css():
    """Test parsing empty CSS."""
    css = ""
    rules = parse_css(css)

    assert len(rules) == 0


def test_parse_css_with_whitespace():
    """Test parsing CSS with various whitespace."""
    css = """

    p   {
        color  :  blue  ;
        margin :10px;
    }

    """
    rules = parse_css(css)

    assert len(rules) == 1
    assert rules[0].selector == "p"
    assert rules[0].declarations["color"] == "blue"
    assert rules[0].declarations["margin"] == "10px"


if __name__ == "__main__":
    test_parse_simple_rule()
    test_parse_multiple_declarations()
    test_parse_multiple_rules()
    test_parse_class_selector()
    test_parse_id_selector()
    test_selector_matches_element()
    test_selector_matches_class()
    test_selector_matches_id()
    test_parse_empty_css()
    test_parse_css_with_whitespace()
    print("All CSS parser tests passed!")
