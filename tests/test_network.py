"""
Tests for DNS resolution.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.network import DNSResolver, resolve_hostname, DNSResolutionError


class TestDNSResolver(unittest.TestCase):
    """Test DNS resolution functionality."""

    def test_resolve_real_hostname(self):
        """Test resolving a real hostname."""
        resolver = DNSResolver()
        ip = resolver.resolve("example.com")

        # example.com should resolve to a valid IP
        self.assertIsNotNone(ip)
        self.assertIsInstance(ip, str)
        # IP should have dots (IPv4 format)
        self.assertIn('.', ip)

    def test_resolve_localhost(self):
        """Test resolving localhost."""
        resolver = DNSResolver()
        ip = resolver.resolve("localhost")

        # localhost should resolve to 127.0.0.1
        self.assertEqual(ip, "127.0.0.1")

    def test_resolve_invalid_hostname(self):
        """Test that invalid hostname raises error."""
        resolver = DNSResolver()

        with self.assertRaises(DNSResolutionError):
            resolver.resolve("this-hostname-definitely-does-not-exist-12345.com")

    def test_cache_works(self):
        """Test that DNS cache works."""
        resolver = DNSResolver()

        # First resolution
        ip1 = resolver.resolve("example.com")

        # Second resolution should come from cache
        ip2 = resolver.resolve("example.com")

        self.assertEqual(ip1, ip2)

        # Verify it's in the cache
        self.assertIn("example.com", resolver._cache)

    def test_clear_cache(self):
        """Test clearing the DNS cache."""
        resolver = DNSResolver()

        # Resolve and cache
        resolver.resolve("example.com")
        self.assertIn("example.com", resolver._cache)

        # Clear cache
        resolver.clear_cache()
        self.assertNotIn("example.com", resolver._cache)

    def test_resolve_hostname_function(self):
        """Test the convenience function."""
        ip = resolve_hostname("example.com")

        self.assertIsNotNone(ip)
        self.assertIsInstance(ip, str)
        self.assertIn('.', ip)

    def test_multiple_resolutions(self):
        """Test resolving multiple different hostnames."""
        resolver = DNSResolver()

        ip1 = resolver.resolve("example.com")
        ip2 = resolver.resolve("localhost")

        # Should get different IPs
        self.assertNotEqual(ip1, ip2)

        # Both should be in cache
        self.assertIn("example.com", resolver._cache)
        self.assertIn("localhost", resolver._cache)


if __name__ == '__main__':
    unittest.main()
