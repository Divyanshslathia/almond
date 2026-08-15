# Learning Log Entry 003: DNS Resolution

**Date**: 2026-08-15  
**Feature**: DNS Resolution  
**Status**: Complete

## What Was Learned

### DNS Is the Internet's Phone Book

Before this feature, we had hostnames like `example.com`. But computers can't connect to names - they need IP addresses like `93.184.216.34`. DNS bridges this gap.

```text
Human: "Take me to example.com"
    ↓
DNS: "example.com is at 93.184.216.34"
    ↓
Computer: "Connecting to 93.184.216.34"
```

### The OS Does the Heavy Lifting

We don't implement the DNS protocol ourselves. The operating system provides DNS resolution through system calls:

```python
socket.gethostbyname("example.com")
```

This Python function:
1. Makes a system call to the OS
2. OS checks its DNS cache
3. If not cached, OS queries DNS servers
4. OS returns IP address to Python

### Caching Is Critical

DNS lookups can take 20-100ms. If we did a DNS lookup for every resource on a page, browsing would be painfully slow. Solution: caching.

We cache at multiple levels:
- **Our application cache** (we implemented this)
- **OS DNS cache** (handled by OS)
- **DNS resolver cache** (ISP's cache)
- **Authoritative server TTL** (how long to cache)

### DNS Resolution Is Blocking

When we call `socket.gethostbyname()`, execution **stops** until the OS returns a result. This can take:
- <1ms (cached)
- 20-100ms (uncached, successful)
- 2-10 seconds (failed, waiting for timeout)

This is why DNS performance matters.

### User Space vs Kernel Space

Our Python code runs in **user space**. The actual DNS protocol implementation (sending UDP packets, parsing DNS responses) happens in **kernel space**.

```text
User Space (our code)
    ↓
System call boundary
    ↓
Kernel Space (OS networking)
    ↓
Network hardware
    ↓
Internet
```

We can't directly send network packets from user space - we must ask the OS to do it.

## Important Discoveries

1. **socket.gethostbyname() is simple but powerful** - One function call abstracts away the entire DNS hierarchy

2. **localhost always resolves to 127.0.0.1** - This is hardcoded in the OS, not a DNS lookup

3. **DNS errors are common** - Typos in hostnames, no internet connection, DNS server down - our code must handle these gracefully

4. **Caching improves performance dramatically** - Second lookup is instant because it's cached

## Questions That Came Up

1. **What is the DNS protocol?** - DNS uses UDP packets (usually) on port 53, with a specific binary format for queries and responses. We're not implementing this - the OS does it for us.

2. **How long should we cache?** - DNS records have TTL (Time To Live) values. For now, our cache lives as long as the resolver object. We'll improve this later.

3. **What about IPv6?** - Modern DNS can return IPv6 addresses (AAAA records). `socket.gethostbyname()` only returns IPv4. For IPv6, we'd use `socket.getaddrinfo()`.

4. **How do DNS servers know the answer?** - DNS is hierarchical: root servers → TLD servers (.com) → authoritative servers (example.com's server). The OS handles this chain for us.

5. **Can one hostname have multiple IPs?** - Yes! This is how load balancing works. `socket.gethostbyname()` returns one IP, but the OS might round-robin between multiple IPs.

## Experiments Conducted

### Experiment 1: Measure DNS lookup time

```python
import time
from browser.network import DNSResolver

resolver = DNSResolver()

# First lookup (uncached)
start = time.time()
resolver.resolve("example.com")
first_time = time.time() - start

# Second lookup (cached)
start = time.time()
resolver.resolve("example.com")
second_time = time.time() - start

print(f"First lookup: {first_time * 1000:.2f}ms")
print(f"Second lookup: {second_time * 1000:.2f}ms")
```

Result: First lookup took ~30ms, second took <1ms. Caching works!

### Experiment 2: What happens with invalid hostname?

```python
try:
    resolve_hostname("this-does-not-exist.com")
except DNSResolutionError as e:
    print(f"Error: {e}")
```

Result: Raises `DNSResolutionError` with clear message. Takes ~2 seconds (timeout).

### Experiment 3: localhost is special

```python
ip = resolve_hostname("localhost")
print(ip)  # 127.0.0.1
```

Result: `localhost` doesn't require actual DNS - the OS has it hardcoded.

## Bugs Encountered

### Bug 1: Not handling DNS errors

**Initial code**: Just called `socket.gethostbyname()` without try/except

**Problem**: If DNS fails, Python raises `socket.gaierror` which isn't user-friendly

**Fix**: Catch `socket.gaierror` and raise our own `DNSResolutionError` with a clear message

```python
try:
    ip_address = socket.gethostbyname(hostname)
except socket.gaierror as e:
    raise DNSResolutionError(f"Failed to resolve {hostname}: {e}")
```

### Bug 2: No caching initially

**Initial code**: Called `socket.gethostbyname()` every time

**Problem**: Repeated lookups for the same hostname were slow

**Fix**: Added `_cache` dictionary to store hostname → IP mappings

**Learning**: Even though the OS caches DNS, application-level caching is still useful because we don't cross the user/kernel boundary.

## Misconceptions Corrected

**Initial thought**: "DNS is complicated - we need to implement the protocol"  
**Corrected**: DNS protocol is complex, but we don't need to implement it. The OS provides everything we need through simple API.

**Initial thought**: "DNS happens once per page load"  
**Corrected**: DNS happens for every unique hostname - including images, scripts, APIs, etc. A single page might trigger 10+ DNS lookups.

**Initial thought**: "We should implement DNS caching with TTL"  
**Corrected**: The OS already does this. Our simple cache is sufficient for now. We can add TTL later if needed.

## Current Limitations

The DNS resolver currently:
- Only returns IPv4 addresses (no IPv6)
- Doesn't respect TTL (caches forever)
- Doesn't handle multiple IPs per hostname
- Doesn't prefetch DNS for linked resources
- Doesn't implement DNS-over-HTTPS
- Doesn't validate that returned value is a valid IP

These limitations are acceptable for now. We're learning core concepts, not building production software.

## What the Next Feature Will Teach

**Feature 4: TCP Connection**

The next feature will teach:
- What TCP is and why it exists
- How TCP differs from UDP
- What a socket is
- How to establish a connection
- The three-way handshake
- What IP addresses and ports mean
- The client-server model
- What "blocking I/O" means
- File descriptors and how the OS manages connections

We'll learn how to take our IP address from DNS and actually connect to the server.

Flow:
```text
DNS Resolution: "93.184.216.34"
    ↓
TCP Connection: socket.connect(("93.184.216.34", 80))
    ↓
Connected socket
    ↓
Ready to send HTTP request
```

## Reflections

DNS feels invisible when you browse the web, but it's critical infrastructure. Every web request starts with DNS.

The key insight: **Names are for humans. IP addresses are for computers. DNS translates between them.**

By implementing DNS resolution (even as a thin wrapper), we understand:
- Why DNS exists
- Where DNS happens (OS, not browser)
- Why DNS performance matters
- How caching helps
- What happens when DNS fails

The abstraction stack is becoming clear:
```text
Our browser code (user space)
    ↓
Python standard library
    ↓
System calls
    ↓
Operating system (kernel space)
    ↓
Network hardware
    ↓
Internet
```

Each layer provides services to the layer above. DNS resolution showed us how user space code leverages kernel space networking through system calls.

Next up: establishing a TCP connection to actually communicate with the server.
