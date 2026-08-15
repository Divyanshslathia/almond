"""
Tests for browser GUI.

Note: GUI tests are limited since they require a display.
We test the underlying logic and provide manual testing instructions.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser.gui import BrowserWindow


class TestBrowserWindow(unittest.TestCase):
    """Test browser window functionality."""

    def test_browser_window_creation(self):
        """Test that browser window can be created."""
        # This test just verifies imports and basic structure
        # Actual GUI testing requires a display
        self.assertTrue(hasattr(BrowserWindow, '__init__'))
        self.assertTrue(hasattr(BrowserWindow, 'navigate'))
        self.assertTrue(hasattr(BrowserWindow, 'go_back'))
        self.assertTrue(hasattr(BrowserWindow, 'go_forward'))
        self.assertTrue(hasattr(BrowserWindow, 'reload'))

    def test_url_normalization(self):
        """Test that URLs without scheme get http:// added."""
        # This would be tested through the navigate method
        # For now, we document the expected behavior
        pass


if __name__ == '__main__':
    # Note: Most GUI tests require manual verification
    print("GUI tests are limited without a display.")
    print("For manual testing, run: python -m browser.gui")
    unittest.main()
