"""
Main entry point for the browser.
"""

from browser.url import parse_url
from browser.network import resolve_hostname
from browser.connection import create_connection
from browser.http import send_request
from browser.response import parse_response


def fetch_page(url_string):
    """
    Fetch a web page from a URL.

    This integrates all the components we've built:
    1. URL parsing
    2. DNS resolution
    3. TCP connection
    4. HTTP request
    5. HTTP response parsing

    Args:
        url_string: Full URL to fetch

    Returns:
        HTTPResponse object

    Example:
        >>> response = fetch_page("http://example.com/")
        >>> print(response.status_code)
        200
        >>> print(response.body[:100])
        b'<!doctype html>...'
    """
    print(f"Fetching: {url_string}")

    # Step 1: Parse URL
    print("  [1/5] Parsing URL...")
    url = parse_url(url_string)
    print(f"        -> {url.scheme}://{url.host}:{url.port}{url.path}")

    # Step 2: Resolve hostname to IP
    print("  [2/5] Resolving DNS...")
    ip = resolve_hostname(url.host)
    print(f"        -> {url.host} = {ip}")

    # Step 3: Establish TCP connection
    print("  [3/5] Connecting to server...")
    with create_connection(ip, url.port, timeout=10) as conn:
        print(f"        -> Connected to {ip}:{url.port}")

        # Step 4: Send HTTP request
        print("  [4/5] Sending HTTP request...")
        send_request(conn, "GET", url.path, url.host)
        print(f"        -> GET {url.path}")

        # Step 5: Receive and parse HTTP response
        print("  [5/5] Receiving response...")
        response_parts = []
        while True:
            chunk = conn.receive(4096)
            if not chunk:
                break
            response_parts.append(chunk)

        response_bytes = b"".join(response_parts)
        response = parse_response(response_bytes)
        print(f"        -> {response.status_code} {response.status_message}")

    print(f"[*] Fetch complete: {len(response.body)} bytes received\n")
    return response


def display_page(response):
    """
    Display a fetched page.

    For now, this just prints the response details and body.
    In a real browser, this would render HTML, execute JavaScript, etc.

    Args:
        response: HTTPResponse object
    """
    print("=" * 70)
    print(f"Status: {response.status_code} {response.status_message}")
    print(f"Version: {response.version}")
    print("=" * 70)

    # Display headers
    if response.headers:
        print("Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print("=" * 70)

    # Display body (decode if text)
    content_type = response.get_header("content-type") or ""
    if "text" in content_type or "html" in content_type:
        # Text content - decode and display
        try:
            body_text = response.body.decode("utf-8", errors="replace")
            print(f"Body ({len(response.body)} bytes):")
            print(body_text)
        except Exception as e:
            print(f"Body ({len(response.body)} bytes): [Could not decode: {e}]")
    else:
        # Binary content - just show size
        print(f"Body: {len(response.body)} bytes (binary content)")

    print("=" * 70)


def main():
    """
    Entry point for the browser application.
    """
    print("=" * 70)
    print("Browser - Built from the Ground Up")
    print("=" * 70)
    print()

    # Default URL to fetch
    url = "http://example.com/"

    # Check for command line argument
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]

    try:
        # Fetch the page
        response = fetch_page(url)

        # Display the page
        display_page(response)

        # Exit status based on HTTP status
        if response.is_success():
            print("\n[*] Success!")
            sys.exit(0)
        else:
            print(f"\n[!] HTTP Error: {response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
