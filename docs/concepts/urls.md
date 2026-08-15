# Concept: URLs (Uniform Resource Locators)

## What is it?

A URL (Uniform Resource Locator) is a string that identifies a resource on the internet and tells your browser how to retrieve it.

Example:
```
http://example.com:80/path/to/page?name=value#section
```

## Why does it exist?

The internet has millions of resources (web pages, images, videos, APIs). We need a standardized way to:

1. **Locate** resources across different servers
2. **Specify** how to retrieve them (HTTP, HTTPS, FTP, etc.)
3. **Navigate** within resources (paths, queries, fragments)

Without URLs, we'd need to remember IP addresses and port numbers for every website.

## What problem does it solve?

**The Problem**: How do we identify and access resources on a distributed network?

**Before URLs**: 
```text
Connect to IP: 93.184.216.34
Port: 80
Send: GET /index.html
```

**With URLs**:
```text
http://example.com/index.html
```

URLs abstract away:
- IP addresses (DNS handles this)
- Port numbers (defaults exist)
- Protocol details (scheme specifies this)

## How does it work?

A URL has this structure:

```text
scheme://host:port/path?query#fragment
```

### Components:

**1. Scheme** (`http`, `https`)
- Tells the browser which protocol to use
- Determines default port (http=80, https=443)

**2. Host** (`example.com`)
- The domain name or IP address
- DNS resolves this to an actual IP address

**3. Port** (`:8080`)
- Optional; defaults based on scheme
- Specifies which port on the server to connect to

**4. Path** (`/path/to/page`)
- Identifies the specific resource on the server
- Always starts with `/`
- Default is `/` if not specified

**5. Query** (`?name=value&other=data`)
- Optional parameters for the request
- Starts with `?`
- Multiple parameters separated by `&`

**6. Fragment** (`#section`)
- Identifies a section within the resource
- Not sent to the server (browser-only)
- Used for in-page navigation

## Where does it sit in the browser?

```text
User types URL
      ↓
URL Parser (we just built this!)
      ↓
Extracts: scheme, host, port, path, query
      ↓
DNS (resolves host to IP)
      ↓
TCP (connects to IP:port)
      ↓
HTTP (sends request for path?query)
      ↓
Response received
```

URL parsing is the **first step** in fetching a web page.

## What does the OS do?

The OS isn't directly involved in URL parsing. This happens in user space within the browser.

However, the OS becomes involved when we use the parsed URL:
- **DNS resolution**: OS may cache DNS results
- **Network connection**: OS manages TCP/IP stack
- **Port binding**: OS tracks which ports are in use

## How does our Python implementation relate to it?

Our implementation manually parses URLs using string operations:

```python
# Split on '://' to get scheme
scheme, rest = url.split('://', 1)

# Split on '?' to get query
if '?' in rest:
    rest, query = rest.split('?', 1)

# Split on '#' to get fragment
if '#' in rest:
    rest, fragment = rest.split('#', 1)
```

This is exactly what high-level libraries like `urllib.parse` do under the hood, but we implement it ourselves to understand the structure.

### Comparison:

**Our implementation**:
```python
from browser.url import parse_url
url = parse_url("http://example.com:8080/path")
print(url.host)  # example.com
print(url.port)  # 8080
```

**Python's urllib**:
```python
from urllib.parse import urlparse
url = urlparse("http://example.com:8080/path")
print(url.hostname)  # example.com
print(url.port)      # 8080
```

The underlying concept is identical.

## What are common misconceptions?

### Misconception 1: "The browser sends the entire URL to the server"
**Reality**: The fragment (`#section`) never leaves the browser. Only scheme, host, port, path, and query are used for the HTTP request.

### Misconception 2: "URLs are just strings"
**Reality**: URLs have structure and rules. Not every string is a valid URL.

### Misconception 3: "http and https are just different names"
**Reality**: They use different protocols (HTTP vs HTTPS), different default ports (80 vs 443), and https includes TLS encryption.

### Misconception 4: "The path is optional"
**Reality**: Every HTTP request has a path. If not specified, it defaults to `/`.

## What should we investigate next?

1. **URL encoding** - How do we handle spaces and special characters in URLs?
2. **Relative vs absolute URLs** - How does `/path` differ from `http://example.com/path`?
3. **URL normalization** - How do we handle `example.com`, `www.example.com`, and `EXAMPLE.COM`?
4. **International domain names** - How do non-ASCII domains work?
5. **URL validation** - What makes a URL valid or invalid?

## Real-World Examples

```text
Simple:
http://example.com
→ scheme: http, host: example.com, port: 80, path: /

With path:
https://github.com/user/repo
→ scheme: https, host: github.com, port: 443, path: /user/repo

With query:
https://google.com/search?q=python
→ query: q=python (tells Google to search for "python")

With fragment:
https://developer.mozilla.org/en-US/docs/Web#Examples
→ fragment: Examples (browser scrolls to that section)
```

## Connection to Browser Operation

When you type a URL in the browser:

```text
1. URL Parser breaks it into components
2. DNS resolves host → IP address
3. TCP connects to IP:port
4. HTTP sends request: GET /path?query HTTP/1.1
5. Server responds with the resource
6. Browser scrolls to #fragment if present
```

URL parsing is step 1. Without it, none of the other steps can happen.
