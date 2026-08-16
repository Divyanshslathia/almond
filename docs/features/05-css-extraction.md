# CSS Extraction and Styling Feature

## Overview

The browser now extracts CSS from `<style>` tags in HTML documents and applies styles to rendered elements.

## Implementation

### CSS Extraction

Added `_extract_css()` method to `gui.py` that:
1. Recursively searches HTML parse tree for `<style>` tags
2. Extracts text content from style tags
3. Passes CSS text to the CSS parser

### CSS Parser (`css_parser.py`)

Parses CSS rules with support for:
- Element selectors (e.g., `p`, `h1`, `div`)
- Class selectors (e.g., `.warning`, `.alert`)
- ID selectors (e.g., `#header`, `#footer`)

Parses declarations into key-value pairs:
```css
p { color: blue; margin: 10px; }
```

### Style Calculation (`style.py`)

Applies CSS rules to DOM elements:
1. Starts with default browser styles for each element type
2. Applies matching CSS rules from `<style>` tags
3. Later rules override earlier ones (simple specificity)

### Default Styles

Built-in styles for common elements:
- Headings: Bold, larger font sizes
- Paragraphs: Block display with margin
- Links: Blue, underlined
- Strong/em: Bold/italic

## Testing

Run unit tests:
- `tests/test_css_parser.py` - CSS parsing
- `tests/test_style.py` - Style calculation

Test visually with `test_pages/css.html` which demonstrates:
- Element selectors
- Class selectors
- Color styling

## Limitations

Current implementation supports:
- Simple selectors only (no combinators)
- Limited set of CSS properties
- No specificity calculation (last rule wins)
- No pseudo-classes or pseudo-elements

This is intentional - the goal is understanding browser fundamentals, not full CSS compatibility.
