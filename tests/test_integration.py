"""
Tests for complete browser integration.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.main import fetch_page


class TestBrowserIntegration(unittest.TestCase):
    """Test complete browser functionality."""

    def test_fetch_example_com(self):
        """Test fetching example.com."""
        response = fetch_page("http://example.com/")

        # Should get successful response
        self.assertTrue(response.is_success())
        self.assertEqual(response.status_code, 200)

        # Should have headers
        self.assertGreater(len(response.headers), 0)

        # Should have body
        self.assertGreater(len(response.body), 0)

        # Body should contain HTML
        body_lower = response.body.lower()
        self.assertIn(b"<html", body_lower)

    def test_fetch_with_path(self):
        """Test fetching with a specific path."""
        response = fetch_page("http://example.com/")

        # Should succeed
        self.assertTrue(response.is_success())

    def test_fetch_https_url_returns_error(self):
        """Test that HTTPS URLs return an error (we don't support TLS yet)."""
        # HTTPS connects to port 443 but we don't do TLS handshake
        # The server returns 400 Bad Request for plain HTTP on HTTPS port
        response = fetch_page("https://example.com/")

        # Should get an error response (not 2xx)
        self.assertFalse(response.is_success())

    def test_end_to_end_pipeline(self):
        """Test the entire pipeline end-to-end."""
        # This test verifies that all components work together:
        # URL parsing → DNS → TCP → HTTP request → HTTP response

        response = fetch_page("http://example.com/")

        # URL parsing worked (we got to this point)
        # DNS worked (we got to this point)
        # TCP connection worked (we got to this point)
        # HTTP request worked (we got a response)
        # HTTP response parsing worked (we have a response object)

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.status_code)
        self.assertIsNotNone(response.body)

        # Should be valid HTTP response
        self.assertGreaterEqual(response.status_code, 100)
        self.assertLess(response.status_code, 600)


if __name__ == '__main__':
    unittest.main()
