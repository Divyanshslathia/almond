"""
Tests for URL parsing.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.url import URL, parse_url


class TestURL(unittest.TestCase):
    """Test URL parsing functionality."""

    def test_simple_http_url(self):
        """Test parsing a simple HTTP URL."""
        url = parse_url("http://example.com")
        self.assertEqual(url.scheme, "http")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.port, 80)
        self.assertEqual(url.path, "/")
        self.assertIsNone(url.query)
        self.assertIsNone(url.fragment)

    def test_https_url(self):
        """Test parsing an HTTPS URL with default port."""
        url = parse_url("https://example.com")
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.port, 443)

    def test_url_with_explicit_port(self):
        """Test URL with explicit port number."""
        url = parse_url("http://example.com:8080")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.port, 8080)

    def test_url_with_path(self):
        """Test URL with path component."""
        url = parse_url("http://example.com/some/path")
        self.assertEqual(url.path, "/some/path")

    def test_url_with_query(self):
        """Test URL with query string."""
        url = parse_url("http://example.com/path?name=value&other=data")
        self.assertEqual(url.path, "/path")
        self.assertEqual(url.query, "name=value&other=data")

    def test_url_with_fragment(self):
        """Test URL with fragment."""
        url = parse_url("http://example.com/path#section")
        self.assertEqual(url.path, "/path")
        self.assertEqual(url.fragment, "section")

    def test_complete_url(self):
        """Test URL with all components."""
        url = parse_url("http://example.com:8080/path/to/page?key=val#frag")
        self.assertEqual(url.scheme, "http")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.port, 8080)
        self.assertEqual(url.path, "/path/to/page")
        self.assertEqual(url.query, "key=val")
        self.assertEqual(url.fragment, "frag")

    def test_url_without_scheme_raises_error(self):
        """Test that URL without scheme raises ValueError."""
        with self.assertRaises(ValueError):
            parse_url("example.com/path")

    def test_url_with_invalid_port_raises_error(self):
        """Test that invalid port raises ValueError."""
        with self.assertRaises(ValueError):
            parse_url("http://example.com:abc")

    def test_url_repr(self):
        """Test URL string representation."""
        url = parse_url("http://example.com:80/path")
        repr_str = repr(url)
        self.assertIn("scheme='http'", repr_str)
        self.assertIn("host='example.com'", repr_str)


if __name__ == '__main__':
    unittest.main()
