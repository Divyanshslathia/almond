"""
TCP connection module.

Establishes TCP socket connections to servers.
This helps understand how sockets and TCP work at a low level.
"""

import socket


class TCPConnection:
    """
    Represents a TCP connection to a server.

    TCP (Transmission Control Protocol) provides:
    - Reliable delivery (packets arrive in order, no duplicates)
    - Connection-oriented (must establish connection first)
    - Bidirectional communication (can send and receive)
    """

    def __init__(self, host, port, timeout=10):
        """
        Initialize a TCP connection.

        Args:
            host: IP address or hostname to connect to
            port: Port number to connect to
            timeout: Connection timeout in seconds (default: 10)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self._connected = False

    def connect(self):
        """
        Establish a TCP connection to the server.

        What happens underneath:
        1. Create a socket (OS allocates file descriptor)
        2. socket.connect() makes a system call
        3. OS initiates TCP three-way handshake:
           - Send SYN (synchronize) packet
           - Receive SYN-ACK (acknowledge)
           - Send ACK
        4. Connection established
        5. Socket is ready for reading/writing

        Raises:
            ConnectionError: If connection fails
            socket.timeout: If connection times out
        """
        try:
            # Create a TCP socket
            # AF_INET = IPv4
            # SOCK_STREAM = TCP (vs SOCK_DGRAM for UDP)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set timeout to avoid hanging forever
            self.socket.settimeout(self.timeout)

            # Connect to the server
            # This blocks until connection succeeds or times out
            # Internally does the TCP three-way handshake
            self.socket.connect((self.host, self.port))

            self._connected = True

        except socket.timeout:
            raise ConnectionError(f"Connection to {self.host}:{self.port} timed out")
        except socket.error as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}: {e}")

    def send(self, data):
        """
        Send data over the connection.

        Args:
            data: Bytes to send

        Returns:
            Number of bytes sent

        Raises:
            ConnectionError: If not connected or send fails
        """
        if not self._connected or self.socket is None:
            raise ConnectionError("Not connected")

        try:
            # Send data
            # This may not send all data at once (TCP can split packets)
            # sendall() ensures all data is sent
            self.socket.sendall(data)
            return len(data)

        except socket.error as e:
            raise ConnectionError(f"Failed to send data: {e}")

    def receive(self, buffer_size=4096):
        """
        Receive data from the connection.

        Args:
            buffer_size: Maximum bytes to receive at once (default: 4096)

        Returns:
            Bytes received (may be empty if connection closed)

        Raises:
            ConnectionError: If not connected or receive fails
        """
        if not self._connected or self.socket is None:
            raise ConnectionError("Not connected")

        try:
            # Receive data
            # This blocks until data arrives or connection closes
            # Returns empty bytes if connection is closed by server
            data = self.socket.recv(buffer_size)
            return data

        except socket.timeout:
            raise ConnectionError("Receive timeout")
        except socket.error as e:
            raise ConnectionError(f"Failed to receive data: {e}")

    def close(self):
        """
        Close the connection.

        What happens underneath:
        1. socket.close() makes a system call
        2. OS initiates TCP connection termination:
           - Send FIN (finish) packet
           - Receive ACK
           - Receive FIN from server
           - Send ACK
        3. Connection closed
        4. OS releases file descriptor
        """
        if self.socket:
            try:
                self.socket.close()
            except socket.error:
                pass  # Already closed
            finally:
                self._connected = False
                self.socket = None

    def is_connected(self):
        """Check if connection is established."""
        return self._connected

    def __enter__(self):
        """Context manager support (with statement)."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
        return False

    def __repr__(self):
        """String representation."""
        status = "connected" if self._connected else "disconnected"
        return f"TCPConnection({self.host}:{self.port}, {status})"


def create_connection(host, port, timeout=10):
    """
    Create and establish a TCP connection.

    Args:
        host: IP address or hostname
        port: Port number
        timeout: Connection timeout in seconds

    Returns:
        Connected TCPConnection object

    Raises:
        ConnectionError: If connection fails

    Example:
        >>> conn = create_connection("93.184.216.34", 80)
        >>> conn.send(b"GET / HTTP/1.1\r\n\r\n")
        >>> response = conn.receive()
        >>> conn.close()
    """
    conn = TCPConnection(host, port, timeout)
    conn.connect()
    return conn
