import unittest

from textnode import TextNode, TextType
from helpers import *

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
        self.assertListEqual(new_nodes, expected_nodes)

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
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://cdn.steamstatic.com/apps/dota2/images/dota_react/dota_footer_logo.png)"
        )
        self.assertListEqual([("image", "https://cdn.steamstatic.com/apps/dota2/images/dota_react/dota_footer_logo.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![dota 2 logo](https://cdn.steamstatic.com/apps/dota2/images/dota_react/logo.png) and ![another dota 2 logo](https://cdn.steamstatic.com/apps/dota2/images/dota_react/logo.png)"
        )
        self.assertListEqual([
                ("dota 2 logo", "https://cdn.steamstatic.com/apps/dota2/images/dota_react/logo.png"),
                ("another dota 2 logo", "https://cdn.steamstatic.com/apps/dota2/images/dota_react/logo.png")
            ], matches)
    
    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links("This is a text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to rvelez dev](https://rvelez.dev)"
        )
        self.assertListEqual([
                ("to rvelez dev", "https://rvelez.dev"), 
            ], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to rvelez dev](https://rvelez.dev) and [to github](https://github.com/rolandovlz/)"
        )
        self.assertListEqual([
                ("to rvelez dev", "https://rvelez.dev"), 
                ("to github", "https://github.com/rolandovlz/")
            ], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    
    
if __name__ == "__main__":
    unittest.main()