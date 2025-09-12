import unittest

from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node

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
    
if __name__ == "__main__":
    unittest.main()