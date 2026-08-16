# Almond Browser

A minimal web browser built from scratch in Python to understand how browsers work.

## What This Is

Almond is a learning project that implements the core components of a web browser without relying on browser libraries. It handles the complete pipeline from URL input to rendered page on screen.

This is not a production browser. It implements a small, controlled subset of web standards to demonstrate browser fundamentals.

## Features

### Networking
- URL parsing and validation
- DNS resolution
- TCP socket connections
- HTTP request/response handling

### Rendering Engine
- HTML tokenization and parsing
- DOM tree construction
- CSS parsing and selector matching
- Style calculation
- Layout engine
- Canvas rendering

### User Interface
- GUI window with address bar
- Clickable links
- Browser history (back/forward)
- Page reload
- Vertical scrolling
- Mouse wheel support

## Installation

### Requirements
- Python 3.8 or higher
- tkinter (included with most Python installations)

### Setup

Clone the repository:
```bash
git clone https://github.com/Divyanshslathia/almond.git
cd almond
```

No additional dependencies required.

## Usage

### Launch the browser

```bash
python src/browser/gui.py
```

### Launch with a URL

```bash
python src/browser/gui.py http://example.com
```

### Test with local pages

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000/test_pages/basic.html` in the browser.

## What It Supports

### HTML Tags
- Document structure: `html`, `head`, `body`, `title`
- Layout: `div`, `span`
- Text: `p`, `h1`, `h2`, `h3`, `strong`, `em`
- Links: `a` with `href`
- Styles: `style` tag

### CSS
- Element selectors: `p`, `div`, `h1`
- Class selectors: `.classname`
- ID selectors: `#idname`
- Common properties: `color`, `font-size`, `margin`, `padding`, `background`

### Interactions
- Click links to navigate
- Back/forward navigation
- Scroll long pages
- Reload current page

## What It Doesn't Support

The browser intentionally omits:
- JavaScript
- Images
- Forms and inputs
- Tables
- Flexbox/Grid
- CSS animations
- HTTPS (HTTP only)
- Cookies
- Cache
- Multiple tabs

This is by design. The goal is understanding browser fundamentals, not feature completeness.

## Architecture

```
URL Input
    ↓
URL Parser → DNS Resolution → TCP Connection → HTTP Request
    ↓
HTTP Response Parser
    ↓
HTML Tokenizer → HTML Parser → DOM Tree
    ↓
CSS Extractor → CSS Parser → Style Calculator
    ↓
Layout Engine
    ↓
Canvas Renderer
    ↓
Display
```

## Project Structure

```
almond/
├── src/browser/
│   ├── url.py           # URL parsing
│   ├── network.py       # DNS resolution
│   ├── connection.py    # TCP connections
│   ├── http.py          # HTTP requests
│   ├── response.py      # HTTP response parsing
│   ├── html_parser.py   # HTML tokenization and parsing
│   ├── dom.py           # DOM tree construction
│   ├── css_parser.py    # CSS parsing
│   ├── style.py         # Style calculation
│   ├── layout.py        # Layout engine
│   ├── gui.py           # Main browser window
│   └── gui_render.py    # Rendering logic
├── tests/               # Unit and integration tests
├── test_pages/          # Local HTML test files
└── docs/                # Documentation
```

## Testing

Run all tests:
```bash
python -m pytest tests/
```

Run specific test modules:
```bash
python tests/test_html_parser.py
python tests/test_css_parser.py
python tests/test_layout.py
```

## Documentation

- **[How To Guide](docs/how_to.md)** - Detailed explanation of how the browser works
- **[Architecture](docs/architecture/)** - System design and component documentation
- **[Features](docs/features/)** - Individual feature documentation
- **[Learning Log](docs/learning-log/)** - Development journey and decisions

## Development

### Adding Features

1. Write tests first
2. Implement the feature
3. Run tests to verify
4. Update documentation
5. Commit with descriptive message

### Debugging

Print DOM tree:
```python
from browser.dom import print_dom_tree
print_dom_tree(dom)
```

Inspect layout:
```python
print(f"Box: x={box.x}, y={box.y}, w={box.width}, h={box.height}")
```

## Learning Path

If you're using this project to learn about browsers:

1. Start with **URL parsing** - Understand how URLs are broken into components
2. Study **networking** - See how HTTP requests work at the socket level
3. Explore **HTML parsing** - Learn tokenization and tree building
4. Understand **DOM** - The tree structure browsers manipulate
5. Learn **CSS** - How styles are parsed and matched
6. Study **layout** - How positions and sizes are calculated
7. See **rendering** - How everything comes together on screen

Each module is intentionally simple and well-commented.

## Why This Exists

Modern browsers are incredibly complex. This project strips away that complexity to show the core concepts:
- How does a URL become a network request?
- How does HTML text become a tree structure?
- How are styles applied to elements?
- How are elements positioned on screen?
- How does clicking a link trigger navigation?

By building a minimal browser, these questions become answerable through direct code reading.

## Limitations and Trade-offs

This browser prioritizes learning over functionality:
- Uses Python instead of C++ for readability
- Implements simple algorithms instead of optimized ones
- Supports minimal HTML/CSS instead of full specs
- Has no security model
- Has no performance optimizations

These trade-offs make the code easier to understand and modify.

## License

MIT License - See LICENSE file for details

## Author

Built as a learning project to understand browser internals from the ground up.

## Acknowledgments

This project is inspired by browser architecture documentation and the principle of learning by building.

---

For detailed information on how the browser works, see the [How To Guide](docs/how_to.md).
