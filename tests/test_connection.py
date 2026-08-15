"""
Tests for TCP connection.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.connection import TCPConnection, create_connection


class TestTCPConnection(unittest.TestCase):
    """Test TCP connection functionality."""

    def test_create_connection_to_example_com(self):
        """Test creating a connection to example.com."""
        # Resolve example.com first
        from browser.network import resolve_hostname
        ip = resolve_hostname("example.com")

        # Connect to port 80 (HTTP)
        conn = create_connection(ip, 80, timeout=5)

        self.assertTrue(conn.is_connected())
        conn.close()
        self.assertFalse(conn.is_connected())

    def test_connection_context_manager(self):
        """Test connection as context manager."""
        from browser.network import resolve_hostname
        ip = resolve_hostname("example.com")

        with create_connection(ip, 80, timeout=5) as conn:
            self.assertTrue(conn.is_connected())

        # Should be closed after context
        self.assertFalse(conn.is_connected())

    def test_send_and_receive(self):
        """Test sending and receiving data."""
        from browser.network import resolve_hostname
        ip = resolve_hostname("example.com")

        with create_connection(ip, 80, timeout=5) as conn:
            # Send a minimal HTTP request
            request = b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
            bytes_sent = conn.send(request)

            self.assertEqual(bytes_sent, len(request))

            # Receive response
            response = conn.receive(4096)

            # Should get some response
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)

            # Should start with HTTP status line
            self.assertTrue(response.startswith(b"HTTP/"))

    def test_connection_to_invalid_ip_fails(self):
        """Test that connection to invalid IP fails."""
        # 192.0.2.1 is reserved for documentation (TEST-NET-1)
        # Should not be routable
        with self.assertRaises(ConnectionError):
            create_connection("192.0.2.1", 80, timeout=2)

    def test_connection_to_invalid_port_fails(self):
        """Test that connection to closed port fails."""
        from browser.network import resolve_hostname
        ip = resolve_hostname("example.com")

        # Port 1 is usually closed
        with self.assertRaises(ConnectionError):
            create_connection(ip, 1, timeout=2)

    def test_send_without_connection_fails(self):
        """Test that sending without connection fails."""
        conn = TCPConnection("example.com", 80)
        # Don't connect

        with self.assertRaises(ConnectionError):
            conn.send(b"test")

    def test_receive_without_connection_fails(self):
        """Test that receiving without connection fails."""
        conn = TCPConnection("example.com", 80)
        # Don't connect

        with self.assertRaises(ConnectionError):
            conn.receive()

    def test_connection_repr(self):
        """Test string representation."""
        conn = TCPConnection("example.com", 80)
        repr_str = repr(conn)

        self.assertIn("example.com", repr_str)
        self.assertIn("80", repr_str)
        self.assertIn("disconnected", repr_str)


if __name__ == '__main__':
    unittest.main()
