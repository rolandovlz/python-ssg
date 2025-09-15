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
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)

def code_block_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [child])

    return ParentNode("pre", [code_node])