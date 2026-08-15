"""
Browser GUI application shell.

Creates a local browser window with address bar and viewport.
Uses tkinter as it's part of Python's standard library.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from browser.url import parse_url
from browser.network import resolve_hostname
from browser.connection import create_connection
from browser.http import send_request
from browser.response import parse_response


class BrowserWindow:
    """
    Main browser window with GUI.

    Components:
    - Address bar for URL input
    - Navigation buttons (back, forward, reload)
    - Viewport for displaying content
    """

    def __init__(self):
        """Initialize the browser window."""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Almond Browser - Built from the Ground Up")
        self.root.geometry("1024x768")

        # Navigation history
        self.history = []
        self.history_index = -1

        # Current page state
        self.current_url = None
        self.current_response = None

        # Build UI components
        self._create_navigation_bar()
        self._create_viewport()

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_navigation_bar(self):
        """Create the navigation bar with address bar and buttons."""
        nav_frame = tk.Frame(self.root, bg="#f0f0f0", height=50)
        nav_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Back button
        self.back_button = tk.Button(
            nav_frame,
            text="←",
            width=3,
            command=self.go_back,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT, padx=2)

        # Forward button
        self.forward_button = tk.Button(
            nav_frame,
            text="→",
            width=3,
            command=self.go_forward,
            state=tk.DISABLED
        )
        self.forward_button.pack(side=tk.LEFT, padx=2)

        # Reload button
        self.reload_button = tk.Button(
            nav_frame,
            text="↻",
            width=3,
            command=self.reload
        )
        self.reload_button.pack(side=tk.LEFT, padx=2)

        # Address bar
        self.address_bar = tk.Entry(nav_frame, font=("Arial", 12))
        self.address_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.address_bar.bind("<Return>", lambda e: self.navigate())

        # Go button
        self.go_button = tk.Button(
            nav_frame,
            text="Go",
            command=self.navigate
        )
        self.go_button.pack(side=tk.LEFT, padx=2)

    def _create_viewport(self):
        """Create the viewport for displaying content."""
        # For now, use a scrolled text widget to display raw content
        # Later this will be replaced with actual rendering
        self.viewport = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="white"
        )
        self.viewport.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def navigate(self, url=None):
        """
        Navigate to a URL.

        Args:
            url: URL to navigate to (if None, use address bar value)
        """
        if url is None:
            url = self.address_bar.get().strip()

        if not url:
            return

        # Add http:// if no scheme
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        try:
            self.status_bar.config(text=f"Loading {url}...")
            self.root.update()

            # Fetch the page
            response = self._fetch_page(url)

            # Update history
            if self.history_index < len(self.history) - 1:
                # Remove forward history when navigating to new page
                self.history = self.history[:self.history_index + 1]

            self.history.append(url)
            self.history_index = len(self.history) - 1

            # Update state
            self.current_url = url
            self.current_response = response

            # Update address bar
            self.address_bar.delete(0, tk.END)
            self.address_bar.insert(0, url)

            # Display the page
            self._display_page(response)

            # Update navigation buttons
            self._update_navigation_buttons()

            self.status_bar.config(text=f"Loaded: {url}")

        except Exception as e:
            self.status_bar.config(text=f"Error: {e}")
            self.viewport.delete(1.0, tk.END)
            self.viewport.insert(1.0, f"Error loading page:\n\n{e}")

    def _fetch_page(self, url_string):
        """
        Fetch a page from a URL.

        Args:
            url_string: URL to fetch

        Returns:
            HTTPResponse object
        """
        # Parse URL
        url = parse_url(url_string)

        # Resolve DNS
        ip = resolve_hostname(url.host)

        # Connect and fetch
        with create_connection(ip, url.port, timeout=10) as conn:
            send_request(conn, "GET", url.path, url.host)

            # Receive response
            response_parts = []
            while True:
                chunk = conn.receive(4096)
                if not chunk:
                    break
                response_parts.append(chunk)

            response_bytes = b"".join(response_parts)
            return parse_response(response_bytes)

    def _display_page(self, response):
        """
        Display a page in the viewport.

        For now, this displays raw HTML.
        Later it will render properly.

        Args:
            response: HTTPResponse object
        """
        self.viewport.delete(1.0, tk.END)

        # Display status
        self.viewport.insert(tk.END, f"Status: {response.status_code} {response.status_message}\n\n")

        # Display body
        try:
            # Try to decode as text
            body_text = response.body.decode("utf-8", errors="replace")
            self.viewport.insert(tk.END, body_text)
        except Exception as e:
            self.viewport.insert(tk.END, f"[Binary content, {len(response.body)} bytes]")

    def go_back(self):
        """Navigate back in history."""
        if self.history_index > 0:
            self.history_index -= 1
            url = self.history[self.history_index]
            self.navigate(url)

    def go_forward(self):
        """Navigate forward in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            url = self.history[self.history_index]
            self.navigate(url)

    def reload(self):
        """Reload the current page."""
        if self.current_url:
            # Don't add to history when reloading
            temp_index = self.history_index
            self.navigate(self.current_url)
            self.history_index = temp_index
            self.history = self.history[:temp_index + 1]

    def _update_navigation_buttons(self):
        """Update the state of navigation buttons based on history."""
        # Back button
        if self.history_index > 0:
            self.back_button.config(state=tk.NORMAL)
        else:
            self.back_button.config(state=tk.DISABLED)

        # Forward button
        if self.history_index < len(self.history) - 1:
            self.forward_button.config(state=tk.NORMAL)
        else:
            self.forward_button.config(state=tk.DISABLED)

    def run(self):
        """Start the browser application."""
        self.root.mainloop()


def launch_browser(url=None):
    """
    Launch the browser application.

    Args:
        url: Optional initial URL to load
    """
    browser = BrowserWindow()

    if url:
        browser.address_bar.insert(0, url)
        browser.navigate()

    browser.run()


if __name__ == "__main__":
    # Get URL from command line if provided
    url = sys.argv[1] if len(sys.argv) > 1 else None
    launch_browser(url)
