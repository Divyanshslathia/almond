"""
DOM (Document Object Model) tree.

Converts HTML parse tree into a DOM structure suitable for styling and layout.
"""

from browser.html_parser import HTMLElement, HTMLText


class DOMNode:
    """Base class for DOM nodes."""

    def __init__(self):
        self.parent = None
        self.children = []

    def add_child(self, child):
        """Add a child node."""
        child.parent = self
        self.children.append(child)


class DOMElement(DOMNode):
    """
    Represents a DOM element.

    This is similar to HTMLElement but designed for the browser engine.
    It will hold computed styles, layout information, etc.
    """

    def __init__(self, tag_name, attributes=None):
        """
        Initialize a DOM element.

        Args:
            tag_name: HTML tag name
            attributes: Dictionary of HTML attributes
        """
        super().__init__()
        self.tag_name = tag_name
        self.attributes = attributes or {}
        self.styles = {}  # Will be populated by style calculation
        self.layout = None  # Will be populated by layout engine

    def get_attribute(self, name, default=None):
        """Get an attribute value."""
        return self.attributes.get(name, default)

    def __repr__(self):
        return f"DOMElement({self.tag_name})"


class DOMText(DOMNode):
    """Represents a text node in the DOM."""

    def __init__(self, text):
        """
        Initialize a text node.

        Args:
            text: Text content
        """
        super().__init__()
        self.text = text

    def __repr__(self):
        return f"DOMText({self.text!r})"


class DOMDocument(DOMNode):
    """
    Represents the document root.

    The top of the DOM tree.
    """

    def __init__(self):
        super().__init__()
        self.tag_name = '#document'

    def __repr__(self):
        return "DOMDocument()"


def build_dom(html_root):
    """
    Build a DOM tree from an HTML parse tree.

    Args:
        html_root: Root HTMLElement from parser

    Returns:
        DOMDocument root

    Example:
        >>> from browser.html_parser import parse_html
        >>> html_root = parse_html("<html><body><p>Hello</p></body></html>")
        >>> dom = build_dom(html_root)
        >>> dom.tag_name
        '#document'
    """
    doc = DOMDocument()

    for child in html_root.children:
        dom_node = _convert_to_dom(child)
        if dom_node:
            doc.add_child(dom_node)

    return doc


def _convert_to_dom(html_node):
    """
    Recursively convert HTML nodes to DOM nodes.

    Args:
        html_node: HTMLElement or HTMLText

    Returns:
        DOMElement or DOMText
    """
    if isinstance(html_node, HTMLText):
        # Convert text node
        # Skip whitespace-only text nodes
        if html_node.text.strip():
            return DOMText(html_node.text)
        return None

    elif isinstance(html_node, HTMLElement):
        # Convert element node
        dom_element = DOMElement(html_node.tag, html_node.attrs)

        # Convert children
        for child in html_node.children:
            dom_child = _convert_to_dom(child)
            if dom_child:
                dom_element.add_child(dom_child)

        return dom_element

    return None


def print_dom_tree(node, indent=0):
    """
    Print a DOM tree for debugging.

    Args:
        node: DOM node to print
        indent: Current indentation level
    """
    prefix = "  " * indent

    if isinstance(node, DOMDocument):
        print(f"{prefix}Document")
    elif isinstance(node, DOMElement):
        attrs_str = ""
        if node.attributes:
            attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in node.attributes.items())
        print(f"{prefix}<{node.tag_name}{attrs_str}>")
    elif isinstance(node, DOMText):
        print(f"{prefix}Text: {node.text!r}")

    # Print children
    for child in node.children:
        print_dom_tree(child, indent + 1)

    if isinstance(node, DOMElement):
        print(f"{prefix}</{node.tag_name}>")
