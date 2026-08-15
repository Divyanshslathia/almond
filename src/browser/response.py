"""
HTTP response parsing module.

Parses HTTP responses to extract status, headers, and body.
"""


class HTTPResponse:
    """
    Represents a parsed HTTP response.

    HTTP response format:
    STATUS_LINE\r\n
    HEADER: value\r\n
    HEADER: value\r\n
    \r\n
    [body]

    Example:
    HTTP/1.1 200 OK\r\n
    Content-Type: text/html\r\n
    Content-Length: 1234\r\n
    \r\n
    <html>...</html>
    """

    def __init__(self, response_bytes):
        """
        Initialize and parse an HTTP response.

        Args:
            response_bytes: Raw response bytes from server
        """
        self.raw = response_bytes
        self.version = None
        self.status_code = None
        self.status_message = None
        self.headers = {}
        self.body = b""

        self._parse()

    def _parse(self):
        """
        Parse the HTTP response into components.

        Process:
        1. Split headers from body (blank line separator)
        2. Parse status line (HTTP/1.1 200 OK)
        3. Parse header lines (Key: Value)
        4. Store body
        """
        # Split headers from body at first blank line (\r\n\r\n)
        if b"\r\n\r\n" in self.raw:
            headers_part, self.body = self.raw.split(b"\r\n\r\n", 1)
        else:
            # No body
            headers_part = self.raw
            self.body = b""

        # Decode headers (HTTP headers are ASCII/UTF-8)
        headers_str = headers_part.decode("utf-8", errors="replace")

        # Split into lines
        lines = headers_str.split("\r\n")

        if not lines:
            raise ValueError("Empty HTTP response")

        # First line is status line: HTTP/1.1 200 OK
        status_line = lines[0]
        self._parse_status_line(status_line)

        # Remaining lines are headers
        for line in lines[1:]:
            if not line:
                continue  # Skip empty lines
            self._parse_header_line(line)

    def _parse_status_line(self, line):
        """
        Parse HTTP status line.

        Format: HTTP/1.1 200 OK
        Parts: version status_code status_message
        """
        parts = line.split(" ", 2)
        if len(parts) < 2:
            raise ValueError(f"Invalid status line: {line}")

        self.version = parts[0]
        self.status_code = int(parts[1])
        self.status_message = parts[2] if len(parts) > 2 else ""

    def _parse_header_line(self, line):
        """
        Parse HTTP header line.

        Format: Content-Type: text/html
        """
        if ":" not in line:
            return  # Skip malformed header

        key, value = line.split(":", 1)
        # Header names are case-insensitive, store lowercase
        self.headers[key.strip().lower()] = value.strip()

    def get_header(self, name):
        """
        Get header value (case-insensitive).

        Args:
            name: Header name

        Returns:
            Header value or None if not present
        """
        return self.headers.get(name.lower())

    def is_success(self):
        """Check if response indicates success (2xx status)."""
        return 200 <= self.status_code < 300

    def is_redirect(self):
        """Check if response is a redirect (3xx status)."""
        return 300 <= self.status_code < 400

    def is_client_error(self):
        """Check if response is a client error (4xx status)."""
        return 400 <= self.status_code < 500

    def is_server_error(self):
        """Check if response is a server error (5xx status)."""
        return 500 <= self.status_code < 600

    def __repr__(self):
        """String representation."""
        return f"HTTPResponse({self.status_code} {self.status_message})"


def parse_response(response_bytes):
    """
    Parse HTTP response bytes.

    Args:
        response_bytes: Raw response from server

    Returns:
        HTTPResponse object

    Example:
        >>> response = parse_response(b"HTTP/1.1 200 OK\r\n\r\nHello")
        >>> response.status_code
        200
        >>> response.body
        b"Hello"
    """
    return HTTPResponse(response_bytes)
