"""
Tests for HTTP requests.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.http import HTTPRequest, send_request, get


class TestHTTPRequest(unittest.TestCase):
    """Test HTTP request functionality."""

    def test_build_simple_get_request(self):
        """Test building a simple GET request."""
        request = HTTPRequest("GET", "/", "example.com")
        request_bytes = request.build()

        # Decode to string for easier testing
        request_str = request_bytes.decode("utf-8")

        # Should have request line
        self.assertIn("GET / HTTP/1.1", request_str)

        # Should have Host header
        self.assertIn("Host: example.com", request_str)

        # Should have Connection header
        self.assertIn("Connection: close", request_str)

        # Should end with blank line
        self.assertTrue(request_str.endswith("\r\n\r\n"))

    def test_build_request_with_path(self):
        """Test building request with path."""
        request = HTTPRequest("GET", "/some/path", "example.com")
        request_bytes = request.build()

        request_str = request_bytes.decode("utf-8")
        self.assertIn("GET /some/path HTTP/1.1", request_str)

    def test_build_request_with_custom_headers(self):
        """Test building request with custom headers."""
        headers = {
            "User-Agent": "TestBrowser/1.0",
            "Accept": "text/html"
        }
        request = HTTPRequest("GET", "/", "example.com", headers=headers)
        request_bytes = request.build()

        request_str = request_bytes.decode("utf-8")
        self.assertIn("User-Agent: TestBrowser/1.0", request_str)
        self.assertIn("Accept: text/html", request_str)

    def test_build_post_request_with_body(self):
        """Test building POST request with body."""
        request = HTTPRequest(
            "POST", "/submit", "example.com",
            body="key=value"
        )
        request_bytes = request.build()

        request_str = request_bytes.decode("utf-8")
        self.assertIn("POST /submit HTTP/1.1", request_str)
        self.assertIn("key=value", request_str)

    def test_method_is_uppercased(self):
        """Test that HTTP method is uppercased."""
        request = HTTPRequest("get", "/", "example.com")
        request_bytes = request.build()

        request_str = request_bytes.decode("utf-8")
        self.assertIn("GET / HTTP/1.1", request_str)

    def test_send_request_to_example_com(self):
        """Test sending a real request to example.com."""
        from browser.network import resolve_hostname
        from browser.connection import create_connection

        ip = resolve_hostname("example.com")

        with create_connection(ip, 80, timeout=5) as conn:
            bytes_sent = send_request(conn, "GET", "/", "example.com")

            self.assertGreater(bytes_sent, 0)

            # Receive response
            response = conn.receive(4096)
            self.assertTrue(response.startswith(b"HTTP/"))

    def test_get_function(self):
        """Test the high-level get() function."""
        response = get("http://example.com/")

        # Should get HTTP response
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

        # Should start with HTTP status line
        self.assertTrue(response.startswith(b"HTTP/1.1"))

        # Should contain status code
        self.assertIn(b"200", response[:20])

    def test_get_function_with_path(self):
        """Test get() with a specific path."""
        response = get("http://example.com/")

        # Should get valid response
        self.assertTrue(response.startswith(b"HTTP/"))
        self.assertIn(b"200", response[:20])

    def test_request_repr(self):
        """Test string representation."""
        request = HTTPRequest("GET", "/page", "example.com")
        repr_str = repr(request)

        self.assertIn("GET", repr_str)
        self.assertIn("example.com", repr_str)
        self.assertIn("/page", repr_str)


if __name__ == '__main__':
    unittest.main()
