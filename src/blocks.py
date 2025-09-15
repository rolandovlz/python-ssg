from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from helpers import text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST ="ordered_list"


def markdown_to_blocks(markdown):
    blocks = []

    sections = markdown.split("\n\n")
    for block in sections:
        stripped_block = block.strip() 
        if not stripped_block:
            continue
        blocks.append(stripped_block)

    return blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if lines[0].startswith(">"):
        for line in lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if lines[0].startswith("- "):
        for line in lines:
            if not line.startswith(f"- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if lines[0].startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node) 
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])

    return ParentNode("pre", [code_node])

def ulist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        item = line[2:]
        children = text_to_children(item)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)

def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        item = line[3:]
        children = text_to_children(item)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    block_content = " ".join(new_lines)
    children = text_to_children(block_content)
    return ParentNode("blockquote", children)
