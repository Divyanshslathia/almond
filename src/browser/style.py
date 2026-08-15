"""
Style calculation.

Applies CSS rules to DOM elements.
"""

from browser.css_parser import selector_matches


DEFAULT_STYLES = {
    'h1': {'font-size': '32px', 'font-weight': 'bold', 'display': 'block', 'margin': '10px 0'},
    'h2': {'font-size': '24px', 'font-weight': 'bold', 'display': 'block', 'margin': '8px 0'},
    'h3': {'font-size': '18px', 'font-weight': 'bold', 'display': 'block', 'margin': '6px 0'},
    'p': {'display': 'block', 'margin': '10px 0'},
    'div': {'display': 'block'},
    'span': {'display': 'inline'},
    'a': {'color': 'blue', 'text-decoration': 'underline'},
    'strong': {'font-weight': 'bold'},
    'em': {'font-style': 'italic'},
    'body': {'margin': '8px'},
}


def calculate_styles(dom_root, css_rules):
    """
    Calculate styles for all elements in DOM tree.

    Args:
        dom_root: DOMDocument root
        css_rules: List of CSSRule objects
    """
    _apply_styles_recursive(dom_root, css_rules)


def _apply_styles_recursive(node, css_rules):
    """Apply styles recursively to node and children."""
    from browser.dom import DOMElement

    if isinstance(node, DOMElement):
        # Start with default styles
        if node.tag_name in DEFAULT_STYLES:
            node.styles = DEFAULT_STYLES[node.tag_name].copy()
        else:
            node.styles = {}

        # Apply CSS rules
        for rule in css_rules:
            if selector_matches(rule.selector, node):
                node.styles.update(rule.declarations)

    # Process children
    for child in node.children:
        _apply_styles_recursive(child, css_rules)
