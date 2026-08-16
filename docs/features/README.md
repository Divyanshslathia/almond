# Features

## Completed Features

### Networking Layer
1. ✅ **Project Skeleton** - Repository structure, entry point, testing - [01-project-skeleton.md](01-project-skeleton.md)
2. ✅ **URL Parsing** - Break URLs into components - [02-url-parsing.md](02-url-parsing.md)
3. ✅ **DNS Resolution** - Resolve hostnames to IP addresses - [03-dns-resolution.md](03-dns-resolution.md)
4. ✅ **TCP Connection** - Establish socket connections
5. ✅ **HTTP Request** - Send manual HTTP requests
6. ✅ **HTTP Response** - Parse HTTP responses
7. ✅ **Fetch Web Page** - Complete pipeline integration

### Browser Engine
8. ✅ **Browser Application Shell** - GUI window with address bar and viewport
9. ✅ **HTML Parser** - Tokenize and parse HTML into tree structure
10. ✅ **DOM Tree** - Convert HTML parse tree to Document Object Model
11. ✅ **CSS Parser** - Parse CSS rules and selectors
12. ✅ **Style Calculation** - Apply CSS rules to DOM elements
13. ✅ **Layout Engine** - Calculate positions and sizes for elements
14. ✅ **Rendering Pipeline** - Paint DOM with styles to canvas
15. ✅ **Link Navigation** - Click links to navigate
16. ✅ **Browser History** - Back/forward navigation
17. ✅ **Scrolling** - Vertical scrolling for long pages - [04-scrolling.md](04-scrolling.md)
18. ✅ **CSS Extraction** - Extract and apply styles from `<style>` tags - [05-css-extraction.md](05-css-extraction.md)

### Testing Infrastructure
19. ✅ **Test Pages** - Local HTML files for deterministic testing - [06-test-pages.md](06-test-pages.md)
20. ✅ **Unit Tests** - Tests for CSS parser, style calculation, and layout

## Current Status

The browser now supports the complete rendering pipeline:
1. Enter URL → Fetch page → Parse HTML → Build DOM
2. Extract CSS → Calculate styles → Perform layout
3. Render to canvas → Handle clicks → Navigate → Scroll

All core features from the CLAUDE.md roadmap are complete.
