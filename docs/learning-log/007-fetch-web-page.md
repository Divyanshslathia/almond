# Learning Log Entry 007: Fetch Web Page

**Date**: 2026-08-15  
**Feature**: Complete Web Page Fetch  
**Status**: Complete

## What Was Learned

### All the Pieces Together

This feature combined everything we built into a working browser:

```text
User enters URL
    ↓
[URL Parser] Extract components
    ↓
[DNS Resolver] hostname → IP address
    ↓
[TCP Connection] Connect to IP:port
    ↓
[HTTP Request] Send GET request
    ↓
[HTTP Response] Parse response
    ↓
Display page
```

Each step was implemented separately, now they work as a pipeline.

### The Complete Flow

When you run `python -m browser.main http://example.com/`:

1. **URL Parsing**: "http://example.com/" → {scheme: "http", host: "example.com", port: 80, path: "/"}
2. **DNS Resolution**: "example.com" → "93.184.216.34"
3. **TCP Connection**: Connect socket to 93.184.216.34:80
4. **HTTP Request**: Send "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
5. **HTTP Response**: Receive and parse response bytes
6. **Display**: Show status, headers, and body

This is the core of how every web browser works.

### Integration Revealed Dependencies

Building the integration revealed:
- Each component depends on the previous one
- Errors anywhere in the pipeline fail the entire fetch
- Good error messages at each step help debugging
- Progress output helps understand what's happening

### A Browser Is Layers of Abstraction

The final browser shows the abstraction layers:

```text
fetch_page() (our high-level function)
    ↓
parse_url() → resolve_hostname() → create_connection() → send_request() → parse_response()
    ↓
Python standard library (socket, etc.)
    ↓
System calls (connect, send, recv)
    ↓
Operating system (TCP/IP stack, DNS resolver)
    ↓
Network hardware
    ↓
Internet
    ↓
Server
```

Each layer provides services to the layer above.

## Important Discoveries

1. **The pipeline is surprisingly simple** - 7 features, ~1000 lines of code total, and we have a working browser

2. **Error handling matters** - Any step can fail (DNS timeout, connection refused, HTTP error), must handle gracefully

3. **Debugging output is valuable** - Showing each step helps understand what's happening

4. **HTTP is chatty** - Even a simple page fetch involves many headers and back-and-forth

5. **The browser doesn't render yet** - We fetch HTML but just display raw text. Rendering (parsing HTML, applying CSS, layout, paint) is a whole other project

## Questions That Came Up

1. **Why doesn't HTTPS work?** - HTTPS requires TLS encryption. We connect to port 443 but send plain HTTP, which the server rejects with 400 Bad Request. TLS is complex (certificates, handshakes, encryption).

2. **What about redirects?** - If server returns 301/302, we should follow the Location header. Not implemented yet.

3. **What about cookies?** - Servers send Set-Cookie headers. We should store and send them back. Not implemented yet.

4. **How do real browsers render HTML?** - Parse HTML → build DOM tree → parse CSS → build style tree → layout → paint → composite. Each is a major undertaking.

5. **What about JavaScript?** - We'd need a JavaScript engine. That's another major project.

## Experiments Conducted

### Experiment 1: Fetch example.com

```bash
python -m browser.main http://example.com/
```

Result: Successfully fetched and displayed the page! Shows status 200, headers, and HTML body.

### Experiment 2: Try HTTPS

```bash
python -m browser.main https://example.com/
```

Result: Connects to port 443 but gets 400 Bad Request because we send plain HTTP instead of doing TLS handshake.

### Experiment 3: Integration test

All 4 integration tests pass:
- Fetch example.com: ✓
- End-to-end pipeline: ✓
- Fetch with path: ✓
- HTTPS returns error: ✓

## Bugs Encountered

### Bug 1: Unicode characters in Windows console

**Problem**: Used Unicode arrows (→) in output, Windows console couldn't display them

**Fix**: Changed to ASCII arrows (->) for compatibility

```python
# Before
print(f"        → {url.host} = {ip}")

# After
print(f"        -> {url.host} = {ip}")
```

### Bug 2: Module import when running main.py directly

**Problem**: `python src/browser/main.py` failed with "No module named 'browser'"

**Fix**: Run as module: `python -m browser.main` or `cd src && python -m browser.main`

## Misconceptions Corrected

**Initial thought**: "Integration will be hard"  
**Corrected**: Integration was straightforward because each component had clear interfaces. Good abstraction made integration easy.

**Initial thought**: "We need to parse HTML to fetch a page"  
**Corrected**: Fetching and rendering are separate. We can fetch HTML as bytes without understanding it.

**Initial thought**: "A browser is one big program"  
**Corrected**: A browser is a pipeline of independent components. Each can be understood separately.

## Current Limitations

The browser currently:
- Only supports HTTP (no HTTPS/TLS)
- Doesn't follow redirects
- Doesn't handle cookies
- Doesn't parse HTML
- Doesn't render anything visually
- Doesn't execute JavaScript
- Doesn't cache responses
- Doesn't handle multiple concurrent requests
- Displays raw HTML instead of rendering

These are all features that real browsers have, but we've accomplished the core: **fetching a web page from the internet**.

## What the Next Features Would Teach

If we continued, the next features would be:

**Feature 8: HTML Parsing** - Parse HTML into a DOM tree
**Feature 9: CSS Parsing** - Parse CSS rules
**Feature 10: Rendering** - Layout and paint HTML
**Feature 11: JavaScript** - Execute scripts
**Feature 12: TLS/HTTPS** - Secure connections

But the 7 features we completed teach the fundamental concepts:
- How URLs work
- How DNS works
- How TCP works
- How HTTP works
- How browsers fetch pages

## Reflections

We built a browser from scratch. It's minimal, but it works. You can type a URL and fetch a real web page from the internet.

The journey revealed:

```text
Understanding > Implementation

We didn't just write code.
We learned:
- Why URLs exist
- How DNS works
- What TCP provides
- How HTTP is structured
- Where the OS fits in
- What system calls do
```

Each feature taught a layer of the internet stack:

```text
Feature 1: Project structure
Feature 2: URLs (application layer)
Feature 3: DNS (application layer, OS services)
Feature 4: TCP (transport layer, via OS)
Feature 5: HTTP request (application layer protocol)
Feature 6: HTTP response (application layer protocol)
Feature 7: Integration (complete pipeline)
```

The key insight: **A browser is not magic. It's a pipeline of well-defined protocols and APIs, each built on the layer below.**

By implementing each step manually, we understand what's really happening when we visit a website.

The browser still has much to learn (rendering, JavaScript, security), but the core mission is complete: **we can fetch a web page and understand how it works underneath**.
