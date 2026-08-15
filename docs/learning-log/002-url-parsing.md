# Learning Log Entry 002: URL Parsing

**Date**: 2026-08-15  
**Feature**: URL Parsing  
**Status**: Complete

## What Was Learned

### URL Structure
URLs are not just strings—they're structured data with specific components:

```text
scheme://host:port/path?query#fragment
```

Each component has meaning:
- **scheme**: Protocol to use
- **host**: Server to contact
- **port**: Service on that server
- **path**: Resource to request
- **query**: Parameters to send
- **fragment**: Section within resource (browser-only)

### String Parsing Techniques

Learned how to parse structured strings by:
1. Working right-to-left for optional components
2. Using `split(separator, maxsplit=1)` to split once
3. Handling missing components with defaults
4. Validating input as we parse

### Protocol Defaults

Different schemes have different defaults:
- **http** → port 80
- **https** → port 443

This is standardized. Browsers automatically use these ports when not specified.

### The Fragment Never Goes to the Server

This was a key insight: the fragment (`#section`) is used only by the browser to scroll to a section. It's never sent in the HTTP request to the server.

```text
User enters: http://example.com/page#intro
Browser sends: GET /page HTTP/1.1
                     ↑ no #intro
```

## Important Discoveries

1. **Order matters in parsing** - Must extract fragment before query, query before path, etc.

2. **String split is powerful** - Most parsing can be done with simple string operations, no regex needed for basic URL parsing

3. **Validation during parsing** - Better to fail fast with clear errors than accept malformed input

4. **Manual parsing reveals structure** - By implementing parsing ourselves, the URL structure became completely clear

## Questions That Came Up

1. **What about URL encoding?** - How do spaces and special characters work? Answer: deferred to later. URLs use percent-encoding (`%20` for space), but we don't need this yet.

2. **What about relative URLs?** - How does `/path` work vs `http://example.com/path`? Answer: relative URLs are resolved against a base URL. Will implement when needed.

3. **Case sensitivity?** - Is `HTTP://EXAMPLE.COM` the same as `http://example.com`? Answer: scheme and host are case-insensitive by spec, but we're not normalizing yet.

4. **What about other schemes?** - ftp://, file://, etc.? Answer: focusing on http/https for now since we're building a web browser.

## Experiments Conducted

Created comprehensive test suite with 10 test cases:

```python
# Test: What if there's no scheme?
parse_url("example.com/path")  # Raises ValueError ✓

# Test: What if port is non-numeric?
parse_url("http://example.com:abc")  # Raises ValueError ✓

# Test: What's the default path?
parse_url("http://example.com")  # path = "/" ✓
```

Experiments revealed:
- Need explicit validation for scheme
- Need to handle default paths
- Need to convert port to integer and catch errors

## Bugs Encountered

### Bug 1: Wrong split order

**Initial code**:
```python
scheme, url = url.split('://', 1)  # First
url, fragment = url.split('#', 1)  # Then this
```

**Problem**: If URL has fragment, splitting scheme fails because `#` is still there.

**Fix**: Extract components right-to-left (fragment → query → scheme → path → port)

### Bug 2: Losing the leading slash in path

**Initial code**:
```python
host_port, path = url.split('/', 1)
# path was "page" instead of "/page"
```

**Fix**: Add back the `/`:
```python
self.path = '/' + path
```

## Misconceptions Corrected

**Initial thought**: "URL parsing is complex and needs regular expressions"  
**Corrected**: Basic URL parsing can be done with simple string splits. Regex is overkill for the common case.

**Initial thought**: "The entire URL goes to the server"  
**Corrected**: The fragment stays in the browser. Only scheme, host, port, path, and query matter for the HTTP request.

**Initial thought**: "Port is always specified"  
**Corrected**: Port is usually implicit. Scheme determines the default.

## Current Limitations

The parser currently:
- Doesn't handle URL encoding (`%20`, `%3A`, etc.)
- Doesn't handle relative URLs
- Doesn't normalize (uppercase/lowercase)
- Doesn't validate host format (could be invalid)
- Doesn't handle IPv6 addresses (`[::1]`)
- Doesn't parse query parameters into key-value pairs
- Doesn't handle all URI schemes (ftp, file, etc.)

These limitations are intentional. We implement features when we need them.

## What the Next Feature Will Teach

**Feature 3: DNS Resolution**

The next feature will teach:
- What DNS is and why it exists
- How hostnames become IP addresses
- What a DNS resolver is
- What the OS networking stack does
- Socket API for DNS lookups
- The difference between user space and kernel space
- Caching and DNS performance

We'll learn how to take the host from our parsed URL and convert it into an IP address we can actually connect to.

Flow:
```text
URL Parser
    ↓
host = "example.com"
    ↓
DNS Resolution
    ↓
IP = "93.184.216.34"
    ↓
Ready for TCP connection
```

## Reflections

Understanding URL parsing reveals how much structure exists in what looks like a simple string. Every piece of a URL has meaning:

```text
http://example.com:80/page?q=test#top
└─┬─┘  └────┬─────┘└┬┘└─┬─┘└──┬──┘└┬┘
  scheme   host    port path  query frag
```

By implementing parsing manually, we saw:
- Why these components exist
- How they're extracted
- What defaults apply
- How validation works

This prepares us for the next step: taking that hostname and resolving it to an IP address through DNS.

The progression is clear:
```text
URL (string)
    ↓ [URL Parser - DONE]
Parsed URL (data structure)
    ↓ [DNS Resolution - NEXT]
IP address
    ↓ [TCP Connection - LATER]
Socket connection
```

Each feature builds on the previous one while teaching a new layer of how the internet works.
