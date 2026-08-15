"""
Layout engine.

Calculates position and size for DOM elements.
"""

from browser.dom import DOMElement, DOMText


class LayoutBox:
    """
    Represents layout information for a DOM node.

    Contains:
    - x, y: Position
    - width, height: Size
    """

    def __init__(self, node):
        self.node = node
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.children = []

    def __repr__(self):
        return f"LayoutBox(x={self.x}, y={self.y}, w={self.width}, h={self.height})"


def calculate_layout(dom_root, viewport_width=800):
    """
    Calculate layout for DOM tree.

    Args:
        dom_root: DOMDocument
        viewport_width: Width of viewport

    Returns:
        Root LayoutBox
    """
    root_box = LayoutBox(dom_root)
    root_box.width = viewport_width

    _layout_children(root_box, 0, 0, viewport_width)

    return root_box


def _layout_children(parent_box, x, y, width):
    """Layout children using simple block layout."""
    current_y = y

    for child in parent_box.node.children:
        if isinstance(child, DOMElement):
            child_box = LayoutBox(child)
            child_box.x = x
            child_box.y = current_y
            child_box.width = width

            # Simple height estimation
            if child.tag_name in ('h1', 'h2', 'h3'):
                child_box.height = 40
            elif child.tag_name == 'p':
                child_box.height = 20
            else:
                child_box.height = 20

            parent_box.children.append(child_box)

            # Layout children
            _layout_children(child_box, x, current_y, width)

            current_y += child_box.height + 5

        elif isinstance(child, DOMText):
            # Text layout (simplified)
            text_box = LayoutBox(child)
            text_box.x = x
            text_box.y = current_y
            text_box.width = width
            text_box.height = 15

            parent_box.children.append(text_box)
            current_y += text_box.height

    # Update parent height
    if parent_box.children:
        last_child = parent_box.children[-1]
        parent_box.height = (last_child.y - y) + last_child.height
