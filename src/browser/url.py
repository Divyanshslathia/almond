"""
URL parsing module.

Parses URLs into their components without using high-level libraries.
This helps understand what URLs actually are and how they're structured.
"""

class URL:
    """
    Represents a parsed URL.

    A URL has the structure:
    scheme://host:port/path?query#fragment

    Example:
    http://example.com:80/page?name=value#section

    Components:
    - scheme: http
    - host: example.com
    - port: 80
    - path: /page
    - query: name=value
    - fragment: section
    """

    def __init__(self, url):
        """
        Initialize a URL object by parsing the URL string.

        Args:
            url: String containing the URL to parse
        """
        self.original = url
        self.scheme = None
        self.host = None
        self.port = None
        self.path = None
        self.query = None
        self.fragment = None

        self._parse()

    def _parse(self):
        """
        Parse the URL into its components.

        This implements manual URL parsing to understand the structure.
        We don't use urllib.parse so we can see what's happening.
        """
        url = self.original

        # Extract fragment (everything after #)
        if '#' in url:
            url, self.fragment = url.split('#', 1)

        # Extract query (everything after ?)
        if '?' in url:
            url, self.query = url.split('?', 1)

        # Extract scheme (everything before ://)
        if '://' in url:
            self.scheme, url = url.split('://', 1)
        else:
            raise ValueError(f"Invalid URL: missing scheme (http:// or https://)")

        # Now we have: host:port/path or host/path or host:port or just host

        # Extract path (everything after first /)
        if '/' in url:
            host_port, self.path = url.split('/', 1)
            self.path = '/' + self.path  # Paths start with /
        else:
            host_port = url
            self.path = '/'  # Default path

        # Extract port (everything after :)
        if ':' in host_port:
            self.host, port_str = host_port.split(':', 1)
            try:
                self.port = int(port_str)
            except ValueError:
                raise ValueError(f"Invalid port: {port_str}")
        else:
            self.host = host_port
            # Set default port based on scheme
            if self.scheme == 'http':
                self.port = 80
            elif self.scheme == 'https':
                self.port = 443
            else:
                self.port = 80  # Default fallback

    def __repr__(self):
        """String representation of the URL object."""
        return (f"URL(scheme={self.scheme!r}, host={self.host!r}, "
                f"port={self.port}, path={self.path!r}, "
                f"query={self.query!r}, fragment={self.fragment!r})")

    def __str__(self):
        """Human-readable string representation."""
        return self.original


def parse_url(url_string):
    """
    Parse a URL string into its components.

    Args:
        url_string: The URL to parse

    Returns:
        URL object with parsed components

    Raises:
        ValueError: If the URL is invalid

    Example:
        >>> url = parse_url("http://example.com:8080/path?query=1#frag")
        >>> url.host
        'example.com'
        >>> url.port
        8080
    """
    return URL(url_string)
