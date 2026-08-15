"""
HTML parser.

Converts HTML strings into a tree of tags and text nodes.
Implements a simple tokenizer and recursive parser.
"""

import re


class HTMLToken:
    """Represents an HTML token."""

    def __init__(self, token_type, data):
        """
        Initialize a token.

        Args:
            token_type: Type of token (TAG_OPEN, TAG_CLOSE, TEXT, etc.)
            data: Token data (tag name, text content, etc.)
        """
        self.type = token_type
        self.data = data

    def __repr__(self):
        return f"HTMLToken({self.type}, {self.data!r})"


class HTMLTokenizer:
    """
    Tokenizes HTML into tags and text.

    Converts:
    <html><body>Hello</body></html>

    Into tokens:
    TAG_OPEN: html
    TAG_OPEN: body
    TEXT: Hello
    TAG_CLOSE: body
    TAG_CLOSE: html
    """

    def __init__(self, html):
        """
        Initialize tokenizer with HTML string.

        Args:
            html: HTML string to tokenize
        """
        self.html = html
        self.pos = 0
        self.tokens = []

    def tokenize(self):
        """
        Tokenize the HTML string.

        Returns:
            List of HTMLToken objects
        """
        while self.pos < len(self.html):
            # Check if we're at a tag
            if self.html[self.pos] == '<':
                self._tokenize_tag()
            else:
                self._tokenize_text()

        return self.tokens

    def _tokenize_tag(self):
        """Tokenize an HTML tag."""
        # Find the end of the tag
        end = self.html.find('>', self.pos)
        if end == -1:
            # Malformed HTML - treat as text
            self.tokens.append(HTMLToken('TEXT', self.html[self.pos:]))
            self.pos = len(self.html)
            return

        # Extract tag content
        tag_content = self.html[self.pos + 1:end]

        # Check if it's a closing tag
        if tag_content.startswith('/'):
            tag_name = tag_content[1:].strip()
            self.tokens.append(HTMLToken('TAG_CLOSE', {'tag': tag_name}))
        # Check if it's a self-closing tag
        elif tag_content.endswith('/'):
            # Parse tag name and attributes
            tag_data = self._parse_tag_content(tag_content[:-1].strip())
            self.tokens.append(HTMLToken('TAG_SELF_CLOSE', tag_data))
        # Regular opening tag
        else:
            # Parse tag name and attributes
            tag_data = self._parse_tag_content(tag_content)
            self.tokens.append(HTMLToken('TAG_OPEN', tag_data))

        self.pos = end + 1

    def _parse_tag_content(self, content):
        """
        Parse tag name and attributes.

        Args:
            content: Tag content (e.g., "a href='http://example.com'")

        Returns:
            Dict with 'tag' and 'attrs'
        """
        # Split on whitespace to separate tag name from attributes
        parts = content.split(None, 1)
        tag_name = parts[0].lower()

        attrs = {}
        if len(parts) > 1:
            attrs = self._parse_attributes(parts[1])

        return {'tag': tag_name, 'attrs': attrs}

    def _parse_attributes(self, attr_string):
        """
        Parse HTML attributes.

        Args:
            attr_string: Attribute string (e.g., "href='url' class='btn'")

        Returns:
            Dict of attribute name -> value
        """
        attrs = {}

        # Simple regex to match name="value" or name='value' or name=value
        pattern = r'(\w+)(?:=(?:"([^"]*)"|\'([^\']*)\'|(\S+)))?'

        for match in re.finditer(pattern, attr_string):
            name = match.group(1).lower()
            # Get the value from whichever quote style was used
            value = match.group(2) or match.group(3) or match.group(4) or ''
            attrs[name] = value

        return attrs

    def _tokenize_text(self):
        """Tokenize text content between tags."""
        # Find the next tag
        next_tag = self.html.find('<', self.pos)

        if next_tag == -1:
            # No more tags - rest is text
            text = self.html[self.pos:]
            self.pos = len(self.html)
        else:
            text = self.html[self.pos:next_tag]
            self.pos = next_tag

        # Only add non-empty text
        text = text.strip()
        if text:
            self.tokens.append(HTMLToken('TEXT', text))


class HTMLNode:
    """Base class for HTML nodes."""

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class HTMLElement(HTMLNode):
    """Represents an HTML element (tag)."""

    def __init__(self, tag, attrs=None):
        """
        Initialize an HTML element.

        Args:
            tag: Tag name (e.g., 'div', 'p', 'a')
            attrs: Dictionary of attributes
        """
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = None

    def add_child(self, child):
        """Add a child node."""
        child.parent = self
        self.children.append(child)

    def __repr__(self):
        return f"HTMLElement({self.tag}, attrs={self.attrs}, children={len(self.children)})"


class HTMLText(HTMLNode):
    """Represents text content."""

    def __init__(self, text):
        """
        Initialize text node.

        Args:
            text: Text content
        """
        self.text = text
        self.parent = None

    def __repr__(self):
        return f"HTMLText({self.text!r})"


class HTMLParser:
    """
    Parses HTML tokens into a tree structure.

    Converts tokens into a tree of HTMLElement and HTMLText nodes.
    """

    def __init__(self, tokens):
        """
        Initialize parser with tokens.

        Args:
            tokens: List of HTMLToken objects
        """
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """
        Parse tokens into HTML tree.

        Returns:
            Root HTMLElement
        """
        # Create a root document element
        root = HTMLElement('document')

        # Parse all top-level elements
        while self.pos < len(self.tokens):
            node = self._parse_node(root)
            if node:
                root.add_child(node)

        return root

    def _parse_node(self, parent):
        """
        Parse a single node (element or text).

        Args:
            parent: Parent element

        Returns:
            HTMLElement or HTMLText or None
        """
        if self.pos >= len(self.tokens):
            return None

        token = self.tokens[self.pos]

        # Text node
        if token.type == 'TEXT':
            self.pos += 1
            return HTMLText(token.data)

        # Self-closing tag
        elif token.type == 'TAG_SELF_CLOSE':
            self.pos += 1
            return HTMLElement(token.data['tag'], token.data['attrs'])

        # Opening tag
        elif token.type == 'TAG_OPEN':
            tag = token.data['tag']
            attrs = token.data['attrs']
            self.pos += 1

            element = HTMLElement(tag, attrs)

            # Parse children until we find the closing tag
            while self.pos < len(self.tokens):
                # Check if next token is our closing tag
                if self.pos < len(self.tokens):
                    next_token = self.tokens[self.pos]
                    if (next_token.type == 'TAG_CLOSE' and
                        next_token.data['tag'] == tag):
                        self.pos += 1  # Consume closing tag
                        break

                # Parse child node
                child = self._parse_node(element)
                if child:
                    element.add_child(child)
                else:
                    break

            return element

        # Closing tag (shouldn't happen at this level, but handle gracefully)
        elif token.type == 'TAG_CLOSE':
            # Return None to signal end of children
            return None

        return None


def parse_html(html_string):
    """
    Parse HTML string into tree structure.

    Args:
        html_string: HTML to parse

    Returns:
        Root HTMLElement

    Example:
        >>> root = parse_html("<html><body><h1>Hello</h1></body></html>")
        >>> root.tag
        'document'
        >>> root.children[0].tag
        'html'
    """
    # Tokenize
    tokenizer = HTMLTokenizer(html_string)
    tokens = tokenizer.tokenize()

    # Parse
    parser = HTMLParser(tokens)
    return parser.parse()
