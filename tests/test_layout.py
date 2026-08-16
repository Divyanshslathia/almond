"""
Tests for layout engine.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.layout import calculate_layout, LayoutBox
from browser.dom import DOMElement, DOMText, DOMDocument


def test_layout_box_creation():
    """Test creating a layout box."""
    p = DOMElement("p")
    box = LayoutBox(p)

    assert box.node == p
    assert box.x == 0
    assert box.y == 0
    assert box.width == 0
    assert box.height == 0
    assert box.children == []


def test_calculate_layout_basic():
    """Test basic layout calculation."""
    root = DOMDocument()
    p = DOMElement("p")
    p.add_child(DOMText("Hello"))
    root.add_child(p)

    layout = calculate_layout(root, viewport_width=800)

    assert layout.width == 800
    assert len(layout.children) == 1


def test_layout_multiple_elements():
    """Test layout with multiple elements."""
    root = DOMDocument()
    p1 = DOMElement("p")
    p1.add_child(DOMText("First"))
    p2 = DOMElement("p")
    p2.add_child(DOMText("Second"))
    root.add_child(p1)
    root.add_child(p2)

    layout = calculate_layout(root, viewport_width=800)

    assert len(layout.children) == 2
    # Second element should be below first
    assert layout.children[1].y > layout.children[0].y


def test_layout_heading_heights():
    """Test that headings get proper heights."""
    root = DOMDocument()
    h1 = DOMElement("h1")
    h2 = DOMElement("h2")
    h3 = DOMElement("h3")
    root.add_child(h1)
    root.add_child(h2)
    root.add_child(h3)

    layout = calculate_layout(root, viewport_width=800)

    # All headings should have height 40 when empty
    assert layout.children[0].height == 40
    assert layout.children[1].height == 40
    assert layout.children[2].height == 40


def test_layout_paragraph_height():
    """Test that paragraphs get proper height."""
    root = DOMDocument()
    p = DOMElement("p")
    root.add_child(p)

    layout = calculate_layout(root, viewport_width=800)

    # Empty paragraph should have height 20
    assert layout.children[0].height == 20


def test_layout_nested_elements():
    """Test layout with nested elements."""
    root = DOMDocument()
    div = DOMElement("div")
    p = DOMElement("p")
    p.add_child(DOMText("Nested"))
    div.add_child(p)
    root.add_child(div)

    layout = calculate_layout(root, viewport_width=800)

    # Div should have child
    div_box = layout.children[0]
    assert len(div_box.children) == 1


def test_layout_text_nodes():
    """Test layout of text nodes."""
    root = DOMDocument()
    text = DOMText("Plain text")
    root.add_child(text)

    layout = calculate_layout(root, viewport_width=800)

    assert len(layout.children) == 1
    text_box = layout.children[0]
    assert text_box.node == text
    assert text_box.height == 15


def test_layout_viewport_width():
    """Test that viewport width is respected."""
    root = DOMDocument()
    p = DOMElement("p")
    p.add_child(DOMText("Text"))
    root.add_child(p)

    layout1 = calculate_layout(root, viewport_width=800)
    layout2 = calculate_layout(root, viewport_width=1200)

    assert layout1.width == 800
    assert layout2.width == 1200
    assert layout1.children[0].width == 800
    assert layout2.children[0].width == 1200


def test_layout_vertical_stacking():
    """Test that elements stack vertically."""
    root = DOMDocument()
    p1 = DOMElement("p")
    p1.add_child(DOMText("First"))
    p2 = DOMElement("p")
    p2.add_child(DOMText("Second"))
    p3 = DOMElement("p")
    p3.add_child(DOMText("Third"))
    root.add_child(p1)
    root.add_child(p2)
    root.add_child(p3)

    layout = calculate_layout(root, viewport_width=800)

    # Each element should be below the previous one
    assert layout.children[0].y == 0
    assert layout.children[1].y > layout.children[0].y
    assert layout.children[2].y > layout.children[1].y


def test_layout_parent_height_calculation():
    """Test that parent height is calculated from children."""
    root = DOMDocument()
    div = DOMElement("div")
    p1 = DOMElement("p")
    p1.add_child(DOMText("First"))
    p2 = DOMElement("p")
    p2.add_child(DOMText("Second"))
    div.add_child(p1)
    div.add_child(p2)
    root.add_child(div)

    layout = calculate_layout(root, viewport_width=800)

    div_box = layout.children[0]
    # Parent height should encompass children
    assert div_box.height > 0


if __name__ == "__main__":
    test_layout_box_creation()
    test_calculate_layout_basic()
    test_layout_multiple_elements()
    test_layout_heading_heights()
    test_layout_paragraph_height()
    test_layout_nested_elements()
    test_layout_text_nodes()
    test_layout_viewport_width()
    test_layout_vertical_stacking()
    test_layout_parent_height_calculation()
    print("All layout tests passed!")
