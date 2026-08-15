"""
Basic tests for the browser package.
"""
import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from browser import __version__

class TestBrowser(unittest.TestCase):
    """Test basic browser setup."""

    def test_version_exists(self):
        """Test that version is defined."""
        self.assertIsNotNone(__version__)
        self.assertEqual(__version__, "0.1.0")

if __name__ == '__main__':
    unittest.main()
