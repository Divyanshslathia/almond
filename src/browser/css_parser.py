"""
CSS Parser.

Parses CSS rules and selectors.
"""

import re


class CSSRule:
    """
    Represents a CSS rule.

    Example:
    p { color: blue; margin: 10px; }

    selector: "p"
    declarations: {"color": "blue", "margin": "10px"}
    """

    def __init__(self, selector, declarations):
        self.selector = selector.strip()
        self.declarations = declarations

    def __repr__(self):
        return f"CSSRule({self.selector}, {self.declarations})"


def parse_css(css_string):
    """
    Parse CSS string into rules.

    Args:
        css_string: CSS to parse

    Returns:
        List of CSSRule objects

    Example:
        >>> rules = parse_css("p { color: blue; }")
        >>> rules[0].selector
        'p'
        >>> rules[0].declarations['color']
        'blue'
    """
    rules = []

    # Simple regex to match rules
    # Matches: selector { declarations }
    pattern = r'([^{]+)\{([^}]+)\}'

    for match in re.finditer(pattern, css_string):
        selector = match.group(1).strip()
        declarations_str = match.group(2).strip()

        # Parse declarations
        declarations = {}
        for decl in declarations_str.split(';'):
            decl = decl.strip()
            if ':' in decl:
                prop, value = decl.split(':', 1)
                declarations[prop.strip()] = value.strip()

        rules.append(CSSRule(selector, declarations))

    return rules


def selector_matches(selector, element):
    """
    Check if a CSS selector matches a DOM element.

    Supports:
    - Element selectors: p, div, h1
    - Class selectors: .classname
    - ID selectors: #idname

    Args:
        selector: CSS selector
        element: DOMElement

    Returns:
        Boolean
    """
    # Element selector
    if not selector.startswith('.') and not selector.startswith('#'):
        return element.tag_name == selector.lower()

    # Class selector
    if selector.startswith('.'):
        class_name = selector[1:]
        element_classes = element.get_attribute('class', '').split()
        return class_name in element_classes

    # ID selector
    if selector.startswith('#'):
        id_name = selector[1:]
        return element.get_attribute('id') == id_name

    return False
