import unittest

from textnode import TextNode, TextType
from helpers import text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://rvelez.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertDictEqual(html_node.props, { "href": "https://rvelez.dev"})

    def test_image(self):
        node = TextNode("dota 2 logo", TextType.IMAGE, "https://cdn.steamstatic.com/apps/dota2/images/dota_react/dota_footer_logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, { "src": "https://cdn.steamstatic.com/apps/dota2/images/dota_react/dota_footer_logo.png", "alt": "dota 2 logo" })

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_delimiter_text_type(self):
        node = TextNode("This is text with a **bold block** word", TextType.BOLD)
        node2 = TextNode("This is text with a _italic block_ word", TextType.ITALIC)
        node3 = TextNode("This is text with a `code block` word", TextType.CODE)
        node4 = TextNode("This is text with a `code block` word", TextType.LINK)
        node5 = TextNode("This is text with a `code block` word", TextType.IMAGE)

        new_nodes = split_nodes_delimiter([node, node2, node3, node4, node5], "`", TextType.CODE)

        expected_nodes = [
            TextNode("This is text with a **bold block** word", TextType.BOLD),
            TextNode("This is text with a _italic block_ word", TextType.ITALIC),
            TextNode("This is text with a `code block` word", TextType.CODE),
            TextNode("This is text with a `code block` word", TextType.LINK),
            TextNode("This is text with a `code block` word", TextType.IMAGE)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    
if __name__ == "__main__":
    unittest.main()