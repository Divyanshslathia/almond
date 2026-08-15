# Feature 3: DNS Resolution

## What We Built

A DNS resolver that converts hostnames to IP addresses using Python's socket API. This is a thin wrapper around the OS's DNS functionality that makes the resolution process explicit and adds application-level caching.

```python
from browser.network import resolve_hostname

ip = resolve_hostname("example.com")
# Returns: "93.184.216.34"
```

## Why We Built It

After parsing a URL, we have a hostname like `example.com`, but we can't connect to a name - we need an IP address. DNS (Domain Name System) bridges this gap by translating human-readable domain names into machine-readable IP addresses.

**The Problem:**
```text
URL Parser gives us: "example.com"
TCP needs: "93.184.216.34"
```

**The Solution:**
```text
"example.com" → [DNS Resolution] → "93.184.216.34"
```

Without DNS, we'd need to remember IP addresses for every website:
- Remember `142.250.185.46` instead of `google.com`
- Remember `140.82.121.4` instead of `github.com`
- Remember `93.184.216.34` instead of `example.com`

## Real-World Flow

```text
User enters URL: http://example.com/page
    ↓
URL Parser extracts: hostname = "example.com"
    ↓
DNS Resolver (this feature!)
    ↓
Check application cache
    ↓
If not cached: call socket.gethostbyname()
    ↓
Python makes system call to OS
    ↓
OS checks its DNS cache
    ↓
If not cached: OS sends DNS query to DNS server (UDP, port 53)
    ↓
DNS server responds with IP: "93.184.216.34"
    ↓
OS caches result and returns to Python
    ↓
Python returns to our code
    ↓
We cache result
    ↓
IP address: "93.184.216.34"
    ↓
Ready for TCP connection
```

### The DNS Hierarchy

When OS queries DNS servers:
```text
Root Server (.)
    ↓ "Ask the .com server"
TLD Server (.com)
    ↓ "Ask example.com's server"
Authoritative Server (example.com)
    ↓ "93.184.216.34"
Your Computer
```

## What Happens Inside the OS

DNS resolution happens at multiple levels:

### User Space (Our Code)
```python
socket.gethostbyname("example.com")
```

### System Call Boundary
Python calls the OS's `getaddrinfo()` system call. This crosses from user space to kernel space.

### Kernel Space (OS DNS Resolver)
1. Check DNS cache
2. If not cached: send UDP packet to DNS server
3. Wait for DNS response
4. Parse DNS response
5. Cache result with TTL
6. Return IP to user space

### Network
- OS sends DNS query via UDP (usually port 53)
- DNS server processes query through DNS hierarchy
- DNS server responds with IP address

### Why System Calls?

User space processes can't directly access the network. Only the kernel can send/receive packets. We must ask the OS to do networking for us through system calls.

```text
Application (user space)
        ↕ [system call boundary]
Kernel (kernel space)
        ↕
Hardware
```

## Python Implementation

### Key Concepts

**socket.gethostbyname()**

Python's socket module provides `gethostbyname()` which:
1. Takes a hostname string
2. Makes a system call to the OS
3. Returns an IP address string

This abstracts away the entire DNS protocol.

**Caching**

We implement application-level caching:
```python
self._cache = {}  # hostname → IP mapping

if hostname in self._cache:
    return self._cache[hostname]  # Instant

# Otherwise: do OS lookup and cache result
```

**Error Handling**

DNS can fail for many reasons:
- Hostname doesn't exist
- No internet connection
- DNS server down
- Network timeout

We catch `socket.gaierror` and raise our own `DNSResolutionError` with clear messages.

### Why Wrap socket.gethostbyname()?

We could call `socket.gethostbyname()` directly, but wrapping it provides:
1. **Explicit DNS step** - Makes resolution visible in our code
2. **Application caching** - Avoid repeated system calls
3. **Better errors** - Clear error messages instead of raw exceptions
4. **Testability** - Can mock DNS for testing
5. **Learning** - Makes DNS resolution an explicit part of our browser

## Code Location

### DNS Module
- **File**: [src/browser/network.py](../../src/browser/network.py)
- **Class**: `DNSResolver`
- **Function**: `resolve_hostname()`

### Tests
- **File**: [tests/test_network.py](../../tests/test_network.py)
- **Coverage**: 7 test cases

## Function-by-Function Explanation

### resolve_hostname(hostname)
- **Location**: `src/browser/network.py`
- **Purpose**: Convenience function for DNS resolution
- **Inputs**: hostname string (e.g., "example.com")
- **Outputs**: IP address string (e.g., "93.184.216.34")
- **Logic**: Creates DNSResolver and calls resolve()
- **Why it exists**: Simple functional interface
- **Called by**: Will be called by connection logic
- **Calls**: `DNSResolver.resolve()`
- **Raises**: `DNSResolutionError` if resolution fails
- **Underlying concept**: User space code requesting kernel space service

### DNSResolver.__init__()
- **Location**: `src/browser/network.py`
- **Purpose**: Initialize resolver with cache
- **Logic**: Creates empty cache dictionary
- **Why it exists**: Store state (cache) for multiple resolutions

### DNSResolver.resolve(hostname)
- **Location**: `src/browser/network.py`
- **Purpose**: Resolve hostname to IP address
- **Inputs**: hostname string
- **Outputs**: IP address string
- **Important logic**:
  1. Check application cache first
  2. If not cached: call `socket.gethostbyname()`
  3. Cache the result
  4. Return IP address
- **Why it exists**: Core DNS resolution with caching
- **Called by**: `resolve_hostname()` or direct usage
- **Calls**: `socket.gethostbyname()` (Python standard library)
- **System calls**: Internally calls OS's `getaddrinfo()`
- **Edge cases**:
  - Hostname not found → raises DNSResolutionError
  - No internet → raises DNSResolutionError
  - Cached result → returns instantly without system call
- **Performance**: 
  - Uncached: 20-100ms
  - Cached: <1ms
- **OS concept**: System call boundary - crossing from user to kernel space

### DNSResolver.clear_cache()
- **Location**: `src/browser/network.py`
- **Purpose**: Clear DNS cache
- **Why it exists**: Testing and debugging

### DNSResolutionError
- **Location**: `src/browser/network.py`
- **Purpose**: DNS-specific exception
- **Why it exists**: Distinguish DNS errors from other errors

## What We're NOT Implementing Yet

- **DNS protocol implementation** - Sending UDP packets, parsing DNS records
- **TTL handling** - Respecting DNS time-to-live
- **IPv6 support** - AAAA records
- **Multiple IPs** - Round-robin for load balancing
- **DNS prefetching** - Resolving hostnames before needed
- **DNSSEC** - DNS security extensions
- **DNS-over-HTTPS** - Encrypted DNS
- **Custom DNS servers** - Using specific DNS resolvers

These are advanced features. We're focusing on understanding core concepts.

## Testing

### Running Tests
```bash
python tests/test_network.py -v
```

### Test Coverage

✅ **Normal Cases**
- Resolve real hostname (example.com)
- Resolve localhost
- Multiple resolutions

✅ **Edge Cases**
- Invalid hostname (should raise error)

✅ **Caching**
- Cache works correctly
- Clear cache works

✅ **Convenience Function**
- `resolve_hostname()` works

All 7 tests passing (took 0.260s due to actual network DNS lookups).

### Manual Testing

```python
from browser.network import resolve_hostname, DNSResolver

# Simple resolution
ip = resolve_hostname("example.com")
print(ip)  # 93.184.216.34

# With caching
resolver = DNSResolver()
import time

start = time.time()
ip1 = resolver.resolve("example.com")
time1 = time.time() - start

start = time.time()
ip2 = resolver.resolve("example.com")  # Cached
time2 = time.time() - start

print(f"First lookup: {time1*1000:.2f}ms")   # ~30ms
print(f"Second lookup: {time2*1000:.2f}ms")  # <1ms
```

## Performance Implications

DNS resolution is a potential bottleneck:

```text
Cached lookup: <1ms
Uncached lookup: 20-100ms
Failed lookup: 2-10 seconds (timeout)
```

A single page might trigger 10+ DNS lookups (for images, scripts, APIs, etc.). Without caching, this would add hundreds of milliseconds to page load time.

This is why:
- We cache aggressively
- OS caches DNS results
- DNS servers cache results
- Some browsers use DNS prefetching

## Integration with URL Parsing

DNS connects to our previous feature:

```python
from browser.url import parse_url
from browser.network import resolve_hostname

# Parse URL
url = parse_url("http://example.com:80/path")

# Resolve hostname
ip = resolve_hostname(url.host)

# Now we have everything needed for TCP connection:
# - IP: "93.184.216.34"
# - Port: 80
# - Path: "/path"
```

## Next Feature

**Feature 4: TCP Connection**

The next feature will teach:
- What TCP is and how it differs from UDP
- What a socket is at the OS level
- How to create and connect a socket
- The TCP three-way handshake
- Client-server model
- Blocking I/O
- File descriptors

We'll take our IP address and port and establish an actual connection to the server.

Flow:
```text
DNS gives us: IP = "93.184.216.34", Port = 80
    ↓
TCP Connection: socket.connect()
    ↓
Three-way handshake: SYN, SYN-ACK, ACK
    ↓
Connected socket
    ↓
Ready to send HTTP request
```
