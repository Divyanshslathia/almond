# Test Pages

## Overview

Local HTML test pages for browser feature verification without depending on external websites.

## Location

`test_pages/` directory in project root.

## Test Files

### basic.html
Simple document with heading and paragraphs. Tests basic rendering pipeline.

### nested.html
Deeply nested div and paragraph elements. Tests DOM tree traversal and layout.

### links.html
Multiple internal and external links. Tests link rendering and navigation.

### css.html
CSS styling with element, class, and ID selectors. Tests CSS extraction and style application.

### layout.html
Various element types and nesting. Tests layout engine calculations.

### long_page.html
Many sections totaling more height than viewport. Tests scrolling functionality.

## Usage

Navigate to test pages using file:// URLs or by starting a local HTTP server:

```bash
python -m http.server 8000
```

Then in the browser:
```
http://localhost:8000/test_pages/basic.html
```

## Purpose

These pages:
- Provide deterministic test cases
- Avoid external dependencies
- Exercise specific browser features
- Use simple HTML the browser can handle

## What They're NOT

These are not compatibility tests. The browser implements a small subset of web standards. Complex modern websites will fail, and that's expected.
