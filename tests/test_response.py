"""
Tests for HTTP response parsing.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.response import HTTPResponse, parse_response


class TestHTTPResponse(unittest.TestCase):
    """Test HTTP response parsing."""

    def test_parse_simple_response(self):
        """Test parsing a simple HTTP response."""
        raw = b"HTTP/1.1 200 OK\r\n\r\n"
        response = parse_response(raw)

        self.assertEqual(response.version, "HTTP/1.1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_message, "OK")
        self.assertEqual(response.body, b"")

    def test_parse_response_with_headers(self):
        """Test parsing response with headers."""
        raw = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html\r\n"
            b"Content-Length: 13\r\n"
            b"\r\n"
            b"Hello, World!"
        )
        response = parse_response(raw)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_header("content-type"), "text/html")
        self.assertEqual(response.get_header("content-length"), "13")
        self.assertEqual(response.body, b"Hello, World!")

    def test_parse_response_with_body(self):
        """Test parsing response with body."""
        raw = b"HTTP/1.1 200 OK\r\n\r\n<html><body>Test</body></html>"
        response = parse_response(raw)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b"<html><body>Test</body></html>")

    def test_parse_404_response(self):
        """Test parsing 404 error response."""
        raw = b"HTTP/1.1 404 Not Found\r\n\r\n"
        response = parse_response(raw)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_message, "Not Found")
        self.assertTrue(response.is_client_error())
        self.assertFalse(response.is_success())

    def test_parse_500_response(self):
        """Test parsing 500 server error."""
        raw = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
        response = parse_response(raw)

        self.assertEqual(response.status_code, 500)
        self.assertTrue(response.is_server_error())
        self.assertFalse(response.is_success())

    def test_parse_redirect_response(self):
        """Test parsing 301 redirect."""
        raw = (
            b"HTTP/1.1 301 Moved Permanently\r\n"
            b"Location: http://example.org/\r\n"
            b"\r\n"
        )
        response = parse_response(raw)

        self.assertEqual(response.status_code, 301)
        self.assertTrue(response.is_redirect())
        self.assertEqual(response.get_header("location"), "http://example.org/")

    def test_header_case_insensitive(self):
        """Test that header lookup is case-insensitive."""
        raw = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response = parse_response(raw)

        self.assertEqual(response.get_header("content-type"), "text/html")
        self.assertEqual(response.get_header("Content-Type"), "text/html")
        self.assertEqual(response.get_header("CONTENT-TYPE"), "text/html")

    def test_status_check_methods(self):
        """Test status checking methods."""
        # Success
        resp_200 = parse_response(b"HTTP/1.1 200 OK\r\n\r\n")
        self.assertTrue(resp_200.is_success())
        self.assertFalse(resp_200.is_redirect())
        self.assertFalse(resp_200.is_client_error())
        self.assertFalse(resp_200.is_server_error())

        # Redirect
        resp_301 = parse_response(b"HTTP/1.1 301 Moved\r\n\r\n")
        self.assertTrue(resp_301.is_redirect())
        self.assertFalse(resp_301.is_success())

        # Client error
        resp_404 = parse_response(b"HTTP/1.1 404 Not Found\r\n\r\n")
        self.assertTrue(resp_404.is_client_error())
        self.assertFalse(resp_404.is_success())

        # Server error
        resp_500 = parse_response(b"HTTP/1.1 500 Error\r\n\r\n")
        self.assertTrue(resp_500.is_server_error())
        self.assertFalse(resp_500.is_success())

    def test_parse_real_response(self):
        """Test parsing response from real server."""
        from browser.http import get

        response_bytes = get("http://example.com/")
        response = parse_response(response_bytes)

        # Should be successful
        self.assertTrue(response.is_success())
        self.assertEqual(response.status_code, 200)

        # Should have headers
        self.assertIsNotNone(response.get_header("content-type"))

        # Should have body
        self.assertGreater(len(response.body), 0)

    def test_response_repr(self):
        """Test string representation."""
        response = parse_response(b"HTTP/1.1 200 OK\r\n\r\n")
        repr_str = repr(response)

        self.assertIn("200", repr_str)
        self.assertIn("OK", repr_str)


if __name__ == '__main__':
    unittest.main()
