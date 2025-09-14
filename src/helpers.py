import re
from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": f"{text_node.url}", "alt": f"{text_node.text}"})

        case _:
            raise Exception(f"Error: Text type '{text_node.text_type}' not found")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_word = node.text.split(delimiter)
        if len(split_word) % 2 == 0:
            raise ValueError("invalid text")
        for i in range(len(split_word)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_word[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_word[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)