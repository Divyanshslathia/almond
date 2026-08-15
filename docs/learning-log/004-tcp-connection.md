# Learning Log Entry 004: TCP Connection

**Date**: 2026-08-15  
**Feature**: TCP Connection  
**Status**: Complete

## What Was Learned

### Sockets Are File Descriptors

A socket is just a file descriptor that represents a network connection. The OS treats sockets like files - you can read from them, write to them, and close them.

```python
socket = socket.socket()  # OS allocates file descriptor
socket.send(data)         # Write to the "file"
data = socket.recv(4096)  # Read from the "file"
socket.close()            # Close the file descriptor
```

### TCP Is Connection-Oriented

Unlike UDP (connectionless), TCP requires establishing a connection before data can be exchanged. This happens through the three-way handshake:

```text
Client                    Server
   |                         |
   |-------- SYN ----------->|  "I want to connect"
   |                         |
   |<----- SYN-ACK ----------|  "OK, I'm ready"
   |                         |
   |-------- ACK ----------->|  "Acknowledged"
   |                         |
   |   Connection Ready      |
```

### Blocking I/O

When we call `socket.connect()` or `socket.recv()`, our program **stops** and waits. This is blocking I/O:

```python
conn.connect((ip, port))  # Blocks until connected or timeout
data = conn.receive()     # Blocks until data arrives
```

This is simple but inefficient for handling multiple connections. Later browsers use non-blocking I/O or async I/O.

### System Calls for Networking

Every network operation crosses the user/kernel boundary:

```text
Python: socket.connect()
    ↓ [system call]
Kernel: Sends SYN packet
Kernel: Waits for SYN-ACK
Kernel: Sends ACK
Kernel: Returns success
    ↓
Python: Connection established
```

Our code can't directly access the network hardware. We must ask the kernel.

### Context Managers for Resource Management

Sockets are system resources that must be cleaned up:

```python
with create_connection(ip, port) as conn:
    conn.send(data)
    # Automatically closed when exiting the block
```

This prevents resource leaks (file descriptor exhaustion).

## Important Discoveries

1. **socket.send() might not send everything** - TCP can split data into multiple packets. That's why we use `sendall()`.

2. **socket.recv() returns empty bytes when connection closes** - This is how we know the server closed the connection.

3. **Timeouts are essential** - Without timeout, a failed connection hangs forever.

4. **Port numbers matter** - HTTP uses port 80, HTTPS uses port 443. Different services use different ports.

5. **Connection failures have many causes** - Network unreachable, connection refused, timeout, etc.

## Questions That Came Up

1. **What is the three-way handshake?** - TCP's way of establishing a connection: SYN, SYN-ACK, ACK. Ensures both sides are ready.

2. **Why AF_INET and SOCK_STREAM?** - AF_INET means IPv4. SOCK_STREAM means TCP (reliable, ordered, connection-oriented).

3. **What happens if we don't close the socket?** - Resource leak. OS has limited file descriptors. Eventually can't open new connections.

4. **Can we reuse a connection?** - Yes! HTTP/1.1 supports connection reuse. We'll implement that later.

5. **What's the difference between TCP and UDP?** - TCP is reliable, ordered, connection-oriented. UDP is unreliable, unordered, connectionless. TCP for web, UDP for DNS/video/gaming.

## Experiments Conducted

### Experiment 1: Connect and send HTTP request

```python
from browser.connection import create_connection
from browser.network import resolve_hostname

ip = resolve_hostname("example.com")
with create_connection(ip, 80) as conn:
    conn.send(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
    response = conn.receive(4096)
    print(response[:100])
```

Result: Got HTTP response starting with `HTTP/1.1 200 OK`! The connection works.

### Experiment 2: Connection timeout

```python
try:
    # 192.0.2.1 is reserved for documentation, not routable
    create_connection("192.0.2.1", 80, timeout=2)
except ConnectionError as e:
    print(f"Failed as expected: {e}")
```

Result: Times out after 2 seconds. Timeout prevents hanging forever.

### Experiment 3: Connection to closed port

```python
ip = resolve_hostname("example.com")
try:
    create_connection(ip, 1, timeout=2)  # Port 1 usually closed
except ConnectionError:
    print("Connection refused")
```

Result: Connection refused immediately. Server actively rejected the connection.

## Bugs Encountered

### Bug 1: Not setting timeout

**Initial code**: Created socket without timeout

**Problem**: If network is down, connection hangs forever

**Fix**: Set timeout on socket
```python
self.socket.settimeout(self.timeout)
```

### Bug 2: Resource warnings in tests

**Problem**: Sockets not always properly closed when exceptions occur

**Fix**: Ensured `close()` is always called in `__exit__` method, even if exceptions occur

### Bug 3: Confusing error messages

**Initial code**: Just re-raised socket errors

**Problem**: `socket.error` messages are cryptic

**Fix**: Catch specific exceptions and provide clear error messages:
```python
except socket.timeout:
    raise ConnectionError(f"Connection to {self.host}:{self.port} timed out")
```

## Misconceptions Corrected

**Initial thought**: "send() sends all data at once"  
**Corrected**: TCP can split data. Use `sendall()` to ensure all data is sent.

**Initial thought**: "Sockets are magic networking objects"  
**Corrected**: Sockets are just file descriptors. The kernel does the actual networking.

**Initial thought**: "Connection failures are rare"  
**Corrected**: Connections fail often - network issues, server down, wrong port, firewall, etc.

## Current Limitations

The TCP connection currently:
- Only supports IPv4 (no IPv6)
- Blocking I/O only (can't handle multiple connections efficiently)
- No connection pooling (creates new connection each time)
- No TLS/SSL support (no HTTPS yet)
- No connection reuse (HTTP/1.1 keep-alive)
- Fixed buffer size for receiving

These will be addressed as needed.

## What the Next Feature Will Teach

**Feature 5: HTTP Request**

The next feature will teach:
- What HTTP is and how it works
- HTTP request format (request line, headers, body)
- How to manually construct HTTP requests
- Bytes and encoding (HTTP is text-based but transmitted as bytes)
- The difference between HTTP/1.0 and HTTP/1.1
- Important HTTP headers

We'll learn how to construct and send an actual HTTP request over our TCP connection.

Flow:
```text
TCP Connection: Connected to 93.184.216.34:80
    ↓
HTTP Request: "GET /page HTTP/1.1\r\nHost: example.com\r\n\r\n"
    ↓
Send bytes over socket
    ↓
Wait for response
```

## Reflections

TCP connections are the foundation of internet communication. Every time you browse the web, your browser establishes TCP connections to servers.

Key insights:
- **Sockets are file descriptors** - The OS provides networking through the file API
- **TCP is reliable but complex** - Three-way handshake, acknowledgments, retransmissions
- **Blocking I/O is simple but limited** - Can't handle many connections efficiently
- **Resources must be managed** - Sockets must be closed to avoid leaks

The abstraction layers are becoming clearer:

```text
Our browser
    ↓
Python socket API
    ↓
System calls (connect, send, recv, close)
    ↓
Kernel TCP/IP stack
    ↓
Network interface
    ↓
Internet
```

We're now ready to use this connection to send HTTP requests and receive responses.
