# How To: Almond Browser

## What This Browser Does

Almond is a minimal web browser built from scratch in Python. It fetches web pages, parses HTML and CSS, calculates layout, and renders content in a GUI window.

## How It Works

### 1. Starting the Browser

```bash
python src/browser/gui.py
```

Or with an initial URL:
```bash
python src/browser/gui.py http://example.com
```

### 2. Navigation Pipeline

When you enter a URL and press Enter:

#### Step 1: Parse URL
```
http://example.com/page.html
   ↓
scheme: http
host: example.com
port: 80
path: /page.html
```

#### Step 2: DNS Resolution
```
example.com → 93.184.216.34
```
Uses system DNS to convert hostname to IP address.

#### Step 3: TCP Connection
```
Create socket → Connect to IP:port → Ready to send
```

#### Step 4: Send HTTP Request
```
GET /page.html HTTP/1.1
Host: example.com
Connection: close
```

#### Step 5: Receive HTTP Response
```
HTTP/1.1 200 OK
Content-Type: text/html

<html>...</html>
```

#### Step 6: Parse HTML
```
<html><body><p>Hello</p></body></html>
   ↓
Token: TAG_OPEN html
Token: TAG_OPEN body
Token: TAG_OPEN p
Token: TEXT Hello
Token: TAG_CLOSE p
...
```

#### Step 7: Build DOM Tree
```
#document
  └─ html
      └─ body
          └─ p
              └─ Text: "Hello"
```

#### Step 8: Extract CSS
```
<style>
  p { color: blue; }
</style>
   ↓
CSSRule(selector="p", declarations={"color": "blue"})
```

#### Step 9: Calculate Styles
```
For each DOM element:
  - Start with default browser styles
  - Apply matching CSS rules
  - Store computed styles on element
```

#### Step 10: Calculate Layout
```
For each element:
  - Calculate x, y position
  - Calculate width, height
  - Layout children recursively
```

#### Step 11: Render to Canvas
```
For each layout box:
  - Draw text with proper font/size/color
  - Draw links in blue and underlined
  - Store clickable areas for links
```

### 3. Interaction

#### Clicking Links
```
Click at (x, y)
  ↓
Check if click is on a link's bounding box
  ↓
Navigate to link's href URL
```

#### Scrolling
```
Mouse wheel or scrollbar drag
  ↓
Update scroll_offset
  ↓
Re-render with new offset
```

#### Back/Forward
```
History: [url1, url2, url3]
Index: 1 (currently at url2)
  ↓
Back: Navigate to url1
Forward: Navigate to url3
```

## File Structure

### Core Modules

```
src/browser/
├── url.py           - Parse URLs into components
├── network.py       - DNS resolution
├── connection.py    - TCP socket connections
├── http.py          - Send HTTP requests
├── response.py      - Parse HTTP responses
├── html_parser.py   - Tokenize and parse HTML
├── dom.py           - Build DOM tree from HTML
├── css_parser.py    - Parse CSS rules
├── style.py         - Apply styles to DOM elements
├── layout.py        - Calculate positions and sizes
├── gui.py           - Main browser window
├── gui_render.py    - Rendering methods
└── main.py          - Command-line entry point
```

### Testing

```
tests/
├── test_url.py          - URL parsing tests
├── test_network.py      - DNS tests
├── test_connection.py   - TCP tests
├── test_http.py         - HTTP request tests
├── test_response.py     - HTTP response tests
├── test_html_parser.py  - HTML parsing tests
├── test_dom.py          - DOM tree tests
├── test_css_parser.py   - CSS parsing tests
├── test_style.py        - Style calculation tests
├── test_layout.py       - Layout engine tests
└── test_integration.py  - End-to-end tests
```

### Test Pages

```
test_pages/
├── basic.html      - Simple heading and paragraphs
├── nested.html     - Nested div and paragraph elements
├── links.html      - Multiple links for navigation testing
├── css.html        - CSS styling demonstration
├── layout.html     - Layout engine testing
└── long_page.html  - Scrolling functionality test
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_css_parser.py
python tests/test_layout.py
python tests/test_style.py
```

## What the Browser Supports

### HTML
- Basic tags: `html`, `head`, `body`, `title`
- Structure: `div`, `span`
- Text: `p`, `h1`, `h2`, `h3`, `strong`, `em`
- Links: `a` with `href` attribute
- Styles: `style` tag

### CSS
- Element selectors: `p`, `div`, `h1`
- Class selectors: `.warning`, `.alert`
- ID selectors: `#header`, `#footer`
- Properties: `color`, `font-size`, `margin`, `padding`, `background`, etc.

### Features
- URL navigation
- Link clicking
- Back/forward history
- Page reload
- Vertical scrolling
- Mouse wheel support

## What the Browser Does NOT Support

- JavaScript
- Images
- Forms
- Tables
- Flexbox/Grid
- Complex CSS (animations, transforms, etc.)
- HTTPS (uses HTTP only)
- Multiple tabs
- Bookmarks
- Cache
- Cookies

This is intentional. The goal is understanding browser fundamentals, not building a production browser.

## Common Issues

### "Connection refused"
- The server might not be running
- Firewall might be blocking the connection
- Try a different URL

### "DNS resolution failed"
- Check internet connection
- Try using IP address directly
- DNS server might be down

### Page doesn't render correctly
- The browser supports only basic HTML/CSS
- Complex modern websites will fail
- Use the test pages in `test_pages/` for reliable testing

### Scrolling doesn't work
- Content might not be tall enough
- Try `test_pages/long_page.html`

## Development Workflow

### Adding a New Feature

1. **Read the relevant code** to understand current implementation
2. **Write tests first** (unit tests for logic, integration tests for pipeline)
3. **Implement the feature** following existing patterns
4. **Run tests** to verify correctness
5. **Update documentation** before committing
6. **Commit** with descriptive message

### Debugging

1. **Print the DOM tree**:
   ```python
   from browser.dom import print_dom_tree
   print_dom_tree(dom)
   ```

2. **Inspect layout boxes**:
   ```python
   print(f"Box: x={box.x}, y={box.y}, w={box.width}, h={box.height}")
   ```

3. **Check HTTP response**:
   ```python
   print(f"Status: {response.status_code}")
   print(f"Headers: {response.headers}")
   print(f"Body: {response.body[:200]}")
   ```

## Architecture

```
User enters URL
        ↓
URL Parser → DNS → TCP Connection → HTTP Request
        ↓
HTTP Response Parser
        ↓
HTML Tokenizer → HTML Parser
        ↓
DOM Tree Builder
        ↓
CSS Extractor → CSS Parser
        ↓
Style Calculator (applies CSS to DOM)
        ↓
Layout Engine (calculates positions/sizes)
        ↓
Renderer (draws to canvas)
        ↓
GUI displays page
```

## Learning Path

If you're exploring this codebase to understand browsers:

1. Start with **URL parsing** (`url.py`) - simplest component
2. Move to **networking** (`network.py`, `connection.py`, `http.py`) - understand the request/response cycle
3. Study **HTML parsing** (`html_parser.py`) - tokenization and tree building
4. Understand **DOM** (`dom.py`) - the tree structure browsers work with
5. Learn **CSS** (`css_parser.py`, `style.py`) - styling and selector matching
6. Explore **layout** (`layout.py`) - how positions and sizes are calculated
7. Finally **rendering** (`gui.py`, `gui_render.py`) - putting it all together

Each module is intentionally simple and readable. Start with the tests to see how each component works in isolation.
