"""
DNS resolution module.

Resolves hostnames to IP addresses using the socket API.
This helps understand how DNS works without using high-level abstractions.
"""

import socket


class DNSResolver:
    """
    Resolves hostnames to IP addresses.

    This wraps Python's socket.gethostbyname() but makes the DNS
    resolution process explicit and understandable.
    """

    def __init__(self):
        """Initialize the DNS resolver."""
        self._cache = {}

    def resolve(self, hostname):
        """
        Resolve a hostname to an IP address.

        Args:
            hostname: Domain name to resolve (e.g., "example.com")

        Returns:
            IP address as a string (e.g., "93.184.216.34")

        Raises:
            socket.gaierror: If the hostname cannot be resolved

        Example:
            >>> resolver = DNSResolver()
            >>> ip = resolver.resolve("example.com")
            >>> print(ip)
            93.184.216.34

        What happens underneath:
        1. Python calls socket.gethostbyname()
        2. Python's socket module makes a system call to the OS
        3. OS checks its DNS cache
        4. If not cached, OS sends DNS query to configured DNS server
        5. DNS server responds with IP address
        6. OS returns IP to Python
        7. We return IP to caller
        """
        # Check our application-level cache first
        if hostname in self._cache:
            return self._cache[hostname]

        try:
            # This is where DNS resolution actually happens.
            # socket.gethostbyname() is a wrapper around the OS's
            # getaddrinfo() system call.
            ip_address = socket.gethostbyname(hostname)

            # Cache the result
            self._cache[hostname] = ip_address

            return ip_address

        except socket.gaierror as e:
            # DNS resolution failed
            # Common causes:
            # - Hostname doesn't exist
            # - No internet connection
            # - DNS server unreachable
            raise DNSResolutionError(f"Failed to resolve {hostname}: {e}")

    def clear_cache(self):
        """Clear the DNS cache."""
        self._cache.clear()


class DNSResolutionError(Exception):
    """Raised when DNS resolution fails."""
    pass


def resolve_hostname(hostname):
    """
    Resolve a hostname to an IP address.

    This is a convenience function that creates a resolver
    and performs the lookup.

    Args:
        hostname: Domain name to resolve

    Returns:
        IP address as a string

    Raises:
        DNSResolutionError: If resolution fails

    Example:
        >>> ip = resolve_hostname("example.com")
        >>> print(ip)
        93.184.216.34
    """
    resolver = DNSResolver()
    return resolver.resolve(hostname)
