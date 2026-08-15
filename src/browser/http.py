"""
HTTP request module.

Constructs and sends HTTP requests manually without using high-level
libraries. This helps understand the HTTP protocol structure.
"""


class HTTPRequest:
    """
    Represents an HTTP request.

    HTTP request format:
    REQUEST_LINE\r\n
    HEADER: value\r\n
    HEADER: value\r\n
    \r\n
    [optional body]

    Example:
    GET /page HTTP/1.1\r\n
    Host: example.com\r\n
    Connection: close\r\n
    \r\n
    """

    def __init__(self, method, path, host, port=80, headers=None, body=None):
        """
        Initialize an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Path to request (e.g., "/index.html")
            host: Hostname (used in Host header)
            port: Port number (default: 80)
            headers: Dictionary of additional headers
            body: Optional request body (for POST, etc.)
        """
        self.method = method.upper()
        self.path = path
        self.host = host
        self.port = port
        self.headers = headers or {}
        self.body = body

    def build(self):
        """
        Build the complete HTTP request as bytes.

        Returns:
            HTTP request as bytes ready to send

        What this does:
        1. Create request line: "GET /path HTTP/1.1"
        2. Add required headers (Host, Connection)
        3. Add user-provided headers
        4. Add blank line (separates headers from body)
        5. Add body if present
        6. Encode everything as bytes (HTTP uses ASCII/UTF-8)
        """
        # Request line: METHOD /path HTTP/1.1
        request_line = f"{self.method} {self.path} HTTP/1.1\r\n"

        # Build headers
        # Host header is required in HTTP/1.1
        headers = {
            "Host": self.host,
            "Connection": "close",  # Close connection after response
        }

        # Add user headers (these can override defaults)
        headers.update(self.headers)

        # Build header lines
        header_lines = ""
        for key, value in headers.items():
            header_lines += f"{key}: {value}\r\n"

        # Blank line marks end of headers
        blank_line = "\r\n"

        # Combine everything
        request_str = request_line + header_lines + blank_line

        # Add body if present
        if self.body:
            if isinstance(self.body, str):
                request_str += self.body
            else:
                # Body is already bytes
                request_bytes = request_str.encode("utf-8")
                return request_bytes + self.body

        # Encode to bytes (HTTP uses UTF-8 for headers)
        return request_str.encode("utf-8")

    def __repr__(self):
        """String representation."""
        return f"HTTPRequest({self.method} {self.host}{self.path})"


def send_request(connection, method, path, host, headers=None, body=None):
    """
    Send an HTTP request over a connection.

    Args:
        connection: TCPConnection object
        method: HTTP method (GET, POST, etc.)
        path: Path to request
        host: Hostname
        headers: Optional additional headers
        body: Optional request body

    Returns:
        Number of bytes sent

    Example:
        >>> from browser.connection import create_connection
        >>> conn = create_connection("93.184.216.34", 80)
        >>> send_request(conn, "GET", "/", "example.com")
        >>> response = conn.receive()
        >>> conn.close()
    """
    request = HTTPRequest(method, path, host, headers=headers, body=body)
    request_bytes = request.build()
    return connection.send(request_bytes)


def get(url_string):
    """
    Perform a GET request to a URL.

    This is a high-level convenience function that combines all
    the components we've built: URL parsing, DNS resolution,
    TCP connection, and HTTP request.

    Args:
        url_string: Full URL to fetch

    Returns:
        Response bytes

    Example:
        >>> response = get("http://example.com/")
        >>> print(response[:100])
        b'HTTP/1.1 200 OK...'
    """
    from browser.url import parse_url
    from browser.network import resolve_hostname
    from browser.connection import create_connection

    # Parse URL
    url = parse_url(url_string)

    # Resolve hostname to IP
    ip = resolve_hostname(url.host)

    # Create connection
    with create_connection(ip, url.port) as conn:
        # Send request
        send_request(conn, "GET", url.path, url.host)

        # Receive response
        response_parts = []
        while True:
            chunk = conn.receive(4096)
            if not chunk:
                break  # Connection closed
            response_parts.append(chunk)

        return b"".join(response_parts)
