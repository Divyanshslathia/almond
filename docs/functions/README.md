# Function Index

This is a central reference for all important functions in the browser.

## Current Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `main()` | [main.py](../../src/browser/main.py) | Entry point for browser |
| `parse_url()` | [url.py](../../src/browser/url.py) | Parse URL string into components |
| `URL._parse()` | [url.py](../../src/browser/url.py) | Internal URL parsing logic |
| `resolve_hostname()` | [network.py](../../src/browser/network.py) | Resolve hostname to IP address |
| `DNSResolver.resolve()` | [network.py](../../src/browser/network.py) | DNS resolution with caching |
| `create_connection()` | [connection.py](../../src/browser/connection.py) | Create TCP connection to server |
| `TCPConnection.connect()` | [connection.py](../../src/browser/connection.py) | Establish TCP connection |
| `TCPConnection.send()` | [connection.py](../../src/browser/connection.py) | Send data over connection |
| `TCPConnection.receive()` | [connection.py](../../src/browser/connection.py) | Receive data from connection |

## About This Index

This index will grow as features are added. Each entry should link directly to the source code and provide a brief description of the function's role.
