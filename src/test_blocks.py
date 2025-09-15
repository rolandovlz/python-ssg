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

    def test_unordered_list(self):
        md = """
- This is a list item
- This is another list item
- This is a third list item with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>This is a list item</li><li>This is another list item</li><li>This is a third list item with <b>bold</b> text</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is a list item
2. This is another list item
3. This is a third list item with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>This is a list item</li><li>This is another list item</li><li>This is a third list item with <b>bold</b> text</li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
> and **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and <b>bold</b> text</blockquote></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

if __name__ == "__main__":
    unittest.main()