# Feature 2: URL Parsing

## What We Built

A URL parser that breaks URLs into their components without using high-level libraries like `urllib.parse`.

Given a URL string like:
```
http://example.com:8080/path/to/page?name=value#section
```

Our parser extracts:
- **scheme**: `http`
- **host**: `example.com`
- **port**: `8080`
- **path**: `/path/to/page`
- **query**: `name=value`
- **fragment**: `section`

## Why We Built It

URLs are the entry point to the web. Before a browser can fetch anything, it must understand what the user is asking for:

- **Which protocol** to use (http, https)
- **Which server** to contact (example.com → DNS → IP address)
- **Which port** to connect to (80, 443, or custom)
- **What resource** to request (/path/to/page)
- **What parameters** to send (?name=value)

By building a URL parser from scratch, we understand that URLs aren't magic strings—they're structured data with specific rules.

## Real-World Flow

```text
User
   ↓
Types: http://example.com/page
   ↓
URL Parser (this feature!)
   ↓
Components: {scheme: http, host: example.com, port: 80, path: /page}
   ↓
These components drive the rest of the browser:
   ↓
DNS: example.com → IP address
   ↓
TCP: Connect to IP:80
   ↓
HTTP: Request /page
```

## What Happens Inside the OS

URL parsing happens entirely in **user space** (our Python process). The OS is not involved.

This is pure string manipulation:
```text
Application (Python)
    ↓
String operations (split, find)
    ↓
Data structures (URL object)
```

The OS only becomes relevant later when we:
- Resolve the hostname (DNS uses OS networking)
- Open a socket (OS manages network connections)
- Send HTTP requests (OS handles TCP/IP)

## Python Implementation

### Key Python Concepts

**String Methods**
- `split(separator, maxsplit)` - Divides string at separator
- `'substring' in string` - Checks for presence

**Manual Parsing Strategy**

We parse in order, stripping components off the URL string:

```python
url = "http://example.com:8080/path?query#fragment"

# 1. Extract fragment (rightmost)
url, fragment = url.split('#', 1)
# url = "http://example.com:8080/path?query"

# 2. Extract query
url, query = url.split('?', 1)
# url = "http://example.com:8080/path"

# 3. Extract scheme
scheme, url = url.split('://', 1)
# scheme = "http", url = "example.com:8080/path"

# 4. Extract path
host_port, path = url.split('/', 1)
# host_port = "example.com:8080", path = "path"

# 5. Extract port
host, port = host_port.split(':', 1)
# host = "example.com", port = "8080"
```

This order matters because:
- Fragment comes after everything else
- Query comes after path but before fragment
- Scheme comes first but we need to remove later components first

### Why maxsplit=1?

```python
url.split('/', 1)  # Split ONCE at first /
```

Without `maxsplit=1`:
```python
"example.com/path/to/page".split('/')
# ['example.com', 'path', 'to', 'page']  ← Too many splits!
```

With `maxsplit=1`:
```python
"example.com/path/to/page".split('/', 1)
# ['example.com', 'path/to/page']  ← Exactly what we want
```

## Code Location

### URL Parser Module
- **File**: [src/browser/url.py](../../src/browser/url.py)
- **Class**: `URL`
- **Function**: `parse_url()`

### Tests
- **File**: [tests/test_url.py](../../tests/test_url.py)
- **Coverage**: 10 test cases covering normal and edge cases

## Function-by-Function Explanation

### parse_url(url_string)
- **Location**: `src/browser/url.py`
- **Purpose**: Entry point for parsing a URL string
- **Inputs**: URL string (e.g., "http://example.com/path")
- **Outputs**: URL object with parsed components
- **Logic**: Creates a URL object, which triggers parsing
- **Why it exists**: Provides a clean functional interface for parsing
- **Called by**: Will be called by the browser's navigation logic
- **Calls**: `URL.__init__()`
- **Edge cases**: Raises ValueError for invalid URLs (missing scheme, invalid port)

### URL.__init__(url)
- **Location**: `src/browser/url.py`
- **Purpose**: Initialize URL object and trigger parsing
- **Inputs**: URL string
- **Outputs**: None (sets object attributes)
- **Logic**: Stores original URL and calls `_parse()`
- **Why it exists**: Constructor for URL objects
- **Called by**: `parse_url()`
- **Calls**: `_parse()`

### URL._parse()
- **Location**: `src/browser/url.py`
- **Purpose**: Perform the actual URL parsing
- **Inputs**: None (operates on `self.original`)
- **Outputs**: None (sets `self.scheme`, `self.host`, etc.)
- **Important logic**:
  1. Extract fragment by splitting on `#`
  2. Extract query by splitting on `?`
  3. Extract scheme by splitting on `://`
  4. Extract path by splitting on first `/`
  5. Extract port by splitting on `:`
  6. Apply default ports for http (80) and https (443)
- **Why it exists**: Encapsulates parsing logic
- **Called by**: `__init__()`
- **Calls**: String methods (`split`, `in`)
- **Important edge cases**:
  - Missing scheme → ValueError
  - Invalid port → ValueError
  - No path → defaults to `/`
  - No port → defaults based on scheme
- **Underlying concept**: String parsing is a fundamental skill in systems programming

### URL.__repr__()
- **Location**: `src/browser/url.py`
- **Purpose**: Debugging representation
- **Outputs**: String showing all components
- **Why it exists**: Makes debugging easier

### URL.__str__()
- **Location**: `src/browser/url.py`
- **Purpose**: Human-readable string
- **Outputs**: Original URL string
- **Why it exists**: Natural string conversion

## What We're NOT Implementing Yet

- **URL encoding** - Handling spaces and special characters (`%20`)
- **Relative URLs** - Paths like `./other` or `../parent`
- **URL normalization** - Treating `example.com` and `EXAMPLE.COM` as equal
- **International domains** - Non-ASCII characters
- **Advanced validation** - Checking against full URL specification
- **Query parsing** - Breaking `?a=1&b=2` into key-value pairs

These will be added when needed.

## Testing

### Running Tests
```bash
python tests/test_url.py -v
```

### Test Coverage

✅ **Normal Cases**
- Simple HTTP URL
- HTTPS URL with default port
- URL with explicit port
- URL with path
- URL with query string
- URL with fragment
- Complete URL with all components

✅ **Edge Cases**
- Missing scheme (should raise ValueError)
- Invalid port (should raise ValueError)

✅ **Verification**
- String representation works correctly

All 10 tests passing.

### Manual Testing

```python
from browser.url import parse_url

# Simple URL
url = parse_url("http://example.com")
print(url.scheme)  # http
print(url.host)    # example.com
print(url.port)    # 80
print(url.path)    # /

# Complex URL
url = parse_url("https://api.github.com:443/repos/user/project?per_page=10#readme")
print(url.scheme)   # https
print(url.host)     # api.github.com
print(url.port)     # 443
print(url.path)     # /repos/user/project
print(url.query)    # per_page=10
print(url.fragment) # readme
```

## Comparison with Standard Library

Our implementation:
```python
from browser.url import parse_url
url = parse_url("http://example.com:8080/path")
```

Python's urllib:
```python
from urllib.parse import urlparse
url = urlparse("http://example.com:8080/path")
```

The concepts are identical. We implemented it ourselves to understand what's happening underneath the abstraction.

## Next Feature

**Feature 3: DNS Resolution**

The next feature will teach:
- What DNS (Domain Name System) is
- Why we need DNS
- How domain names become IP addresses
- What a resolver is
- What the operating system does
- Socket API for DNS lookups
- The difference between user space and kernel space networking

We'll take the `host` from our parsed URL and resolve it to an IP address that we can actually connect to.

Flow:
```text
URL Parser: "example.com" (hostname)
      ↓
DNS Resolution
      ↓
"93.184.216.34" (IP address)
      ↓
Ready for TCP connection
```
