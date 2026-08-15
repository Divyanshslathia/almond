# Concept: DNS (Domain Name System)

## What is it?

DNS (Domain Name System) is the internet's phone book. It translates human-readable domain names like `example.com` into machine-readable IP addresses like `93.184.216.34`.

```text
example.com  →  [DNS]  →  93.184.216.34
```

## Why does it exist?

Computers communicate using IP addresses (e.g., `93.184.216.34`), but humans can't remember thousands of numeric addresses. DNS solves this problem by providing a name-to-address mapping service.

**Without DNS:**
```text
Visit Google: Type 142.250.185.46
Visit GitHub: Type 140.82.121.4
Visit Wikipedia: Type 208.80.154.224
```

**With DNS:**
```text
Visit Google: Type google.com
Visit GitHub: Type github.com
Visit Wikipedia: Type wikipedia.org
```

## What problem does it solve?

### Problem 1: Human Memory
People can't remember IP addresses for every website they visit.

### Problem 2: Server Changes
If a website moves to a different server (new IP), DNS can be updated without changing the domain name. Users don't need to know anything changed.

### Problem 3: Load Balancing
One domain name can map to multiple IP addresses for distributing traffic across servers.

### Problem 4: Global Distribution
Different regions can get different IPs for the same domain, directing users to nearby servers.

## How does it work?

### The DNS Hierarchy

DNS is a distributed hierarchical system:

```text
Root DNS Servers (.)
        ↓
Top-Level Domain Servers (.com, .org, .net)
        ↓
Authoritative Name Servers (example.com)
        ↓
Your IP Address
```

### DNS Resolution Process

When you look up `example.com`:

```text
1. Your computer
   ↓
2. Operating system DNS cache (checked first)
   ↓
3. If not cached: OS contacts DNS resolver (usually your ISP's)
   ↓
4. Resolver checks its cache
   ↓
5. If not cached: Resolver queries root server
   ↓
6. Root server says: "Ask the .com server"
   ↓
7. Resolver queries .com server
   ↓
8. .com server says: "Ask example.com's authoritative server"
   ↓
9. Resolver queries example.com's server
   ↓
10. Authoritative server responds with IP: 93.184.216.34
    ↓
11. Resolver caches the result and returns it to OS
    ↓
12. OS caches the result and returns it to your application
    ↓
13. Your browser can now connect to 93.184.216.34
```

This seems complex, but it usually takes milliseconds due to caching at multiple levels.

## Where does it sit in the browser?

```text
User types URL
    ↓
URL Parser extracts hostname
    ↓
DNS Resolver (we just built this!)
    ↓
Operating System DNS resolver
    ↓
Network → DNS servers
    ↓
IP address returned
    ↓
TCP connection can be established
```

DNS resolution happens **before** any network connection to the target server.

## What does the OS do?

The OS provides the actual DNS infrastructure:

### OS Responsibilities:
1. **Maintains DNS cache** - Previously resolved names are cached
2. **Contacts DNS servers** - Sends DNS queries over UDP (usually port 53)
3. **Handles retries** - If DNS server doesn't respond, tries others
4. **Returns results** - Provides IP address to application

### System Calls:
When we call Python's `socket.gethostbyname()`, Python makes a system call (usually `getaddrinfo()`) to the OS kernel. The kernel handles all the DNS protocol details.

```text
Python: socket.gethostbyname("example.com")
    ↓
System call: getaddrinfo()
    ↓
Kernel: DNS resolution logic
    ↓
Network: UDP packets to DNS server
    ↓
DNS Server: Responds with IP
    ↓
Kernel: Returns IP to Python
    ↓
Python: Returns IP to our code
```

We're operating in **user space**. The actual DNS protocol (sending UDP packets, parsing DNS records) happens in **kernel space**.

## How does our Python implementation relate to it?

Our implementation wraps the OS's DNS functionality:

```python
from browser.network import resolve_hostname

ip = resolve_hostname("example.com")
# Returns: "93.184.216.34"
```

Under the hood:
```python
socket.gethostbyname("example.com")
```

We're not implementing the DNS protocol itself (that would require sending UDP packets, parsing DNS records, handling the hierarchy, etc.). Instead, we:
1. Use the OS's DNS resolver
2. Add our own application-level cache
3. Provide clear error handling
4. Make the DNS resolution step explicit

### Why not implement DNS protocol ourselves?

We could implement the DNS protocol (RFC 1035), but that would involve:
- Understanding UDP sockets
- Parsing binary DNS packet format
- Handling the DNS hierarchy
- Implementing caching and TTL
- Handling DNS security (DNSSEC)

This would be educational, but it's not necessary to understand how browsers work. The key insight is:

> **Hostnames must be resolved to IP addresses before we can connect.**

## What are common misconceptions?

### Misconception 1: "DNS happens once when you type a URL"
**Reality**: DNS happens for every hostname - including embedded resources, redirects, API calls, etc.

### Misconception 2: "DNS is slow"
**Reality**: DNS is heavily cached. The first lookup might take 20-100ms, but subsequent lookups are instant (from cache).

### Misconception 3: "DNS just returns one IP"
**Reality**: DNS can return multiple IPs for load balancing and redundancy.

### Misconception 4: "The browser does DNS"
**Reality**: The OS does DNS. The browser just asks the OS.

### Misconception 5: "DNS uses TCP"
**Reality**: DNS primarily uses UDP (port 53). TCP is only used for large responses or zone transfers.

## What should we investigate next?

1. **DNS caching TTL** - How long should we cache DNS results?
2. **DNS records** - A records, CNAME records, MX records, etc.
3. **IPv6** - DNS can return IPv6 addresses (AAAA records)
4. **DNS security** - DNSSEC, DNS over HTTPS (DoH)
5. **DNS failures** - What happens when DNS doesn't work?
6. **Split-horizon DNS** - Different IPs for internal vs external users

## Real-World Examples

### Example 1: Visiting a website
```text
You type: https://github.com
    ↓
Browser: DNS lookup for "github.com"
    ↓
DNS: Returns 140.82.121.4
    ↓
Browser: Connects to 140.82.121.4:443
```

### Example 2: Load balancing
```text
DNS lookup: google.com
DNS returns: [142.250.185.46, 142.250.185.78, 142.250.185.110]
Browser: Picks one IP to connect to
```

### Example 3: Caching
```text
First visit to example.com: 50ms (DNS lookup)
Second visit: 0ms (cached)
Third visit: 0ms (still cached)
After 5 minutes: 30ms (cache expired, new lookup)
```

## Connection to Browser Operation

DNS is step 2 in fetching a web page:

```text
1. Parse URL → extract hostname
2. DNS resolution → get IP address [WE ARE HERE]
3. TCP connection → connect to IP:port
4. HTTP request → fetch the resource
5. Parse response → display content
```

Without DNS, we couldn't convert `example.com` to `93.184.216.34`, and we couldn't establish a connection.

## Performance Implications

DNS can impact browser performance:

```text
Cached DNS lookup: <1ms
Uncached DNS lookup: 20-100ms
Failed DNS lookup: 2-10 seconds (timeouts)
```

This is why:
- Browsers cache DNS aggressively
- Operating systems cache DNS
- DNS servers cache results
- Some sites use DNS prefetching

A slow DNS lookup can make a fast website feel slow.

## Security Considerations

DNS has security implications:

1. **DNS spoofing** - Attacker returns wrong IP
2. **DNS hijacking** - ISP redirects failed lookups to ads
3. **DNS leaks** - VPN doesn't protect DNS queries
4. **DNS poisoning** - Cache is contaminated with wrong data

These are why DNSSEC and DNS-over-HTTPS exist.
