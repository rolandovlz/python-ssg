import unittest
from blocks import *

class TestBlocks(unittest.TestCase):
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "##### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = "This is a **bolded** paragraph"
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)

    def test_block_to_block_type_ul(self):
        block = "- This is a multiline ul\n- Another list item"
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_fake_ul(self):
        block = "- This is a multiline ul\n- Another list item\nNot list item, should return paragraph type"
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_ol(self):
        block = "1. First item\n2. Second item\n3. Ordered list"
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.ORDERED_LIST)
    
    
   

    

if __name__ == "__main__":
    unittest.main()