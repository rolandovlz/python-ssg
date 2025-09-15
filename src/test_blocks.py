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
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 

   
if __name__ == "__main__":
    unittest.main()