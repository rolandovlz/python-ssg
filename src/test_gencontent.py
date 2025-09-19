import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        md = """
## Subtitle
# Title

markdown content
"""
        response = extract_title(md)
        self.assertEqual("Title", response)

    def test_extract_title_no_title(self):
        md = """
## Subtitle

markdown content
"""
        self.assertRaises(ValueError, extract_title, md )

if __name__ == "__main__":
    unittest.main()