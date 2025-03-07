from enum import Enum
from functions import text_to_textnodes, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks_out = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip('\n')
        #block = block.replace('\n', ' ')
        #print(block)
        blocks_out.append(block)
    #print(blocks_out)
    return blocks_out

def block_to_block_type(block):
    if "#" in block:
        return BlockType.HEADING
    elif "```" in block:
        return BlockType.CODE
    elif ">" in block:
        return BlockType.QUOTE
    elif "- " in block:
        return BlockType.UNORDERED_LIST
    elif "1. " in block:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def make_children_nodes(nodes):
    #print(f"NODES: {nodes}")
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def replace_markdown(markdown, text):
    return markdown.replace(text, "")

def which_heading(block):
    if "######" in block:
        text = replace_markdown(block, "######")
        tag = "h6"
    elif "#####" in block:
        text = replace_markdown(block, "#####")
        tag = "h5"
    elif "####" in block:
        text = replace_markdown(block, "####")
        tag = "h4"
    elif "###" in block:
        text = replace_markdown(block, "###")
        tag = "h3"
    elif "##" in block:
        text = replace_markdown(block, "##")
        tag = "h2"
    else:
        text = replace_markdown(block, "#")
        tag = "h1"
    return text,tag

def make_list_items(items):
    results = []
    for item in items:
        if item != "":
            results.append(block_to_parent(item, "li"))
    return results

def remove_number_and_period(string):
    list_items = re.findall(r'\d+\.\s*[^0-9]+', string)
    cleaned_list_items = [re.sub(r'^\d+\.\s*', '', item) for item in list_items]
    html_nodes = make_list_items(cleaned_list_items)
    return html_nodes

def block_to_parent(block,tag):
    nodes = text_to_textnodes(block)
    html_nodes = make_children_nodes(nodes)
    block_parent = ParentNode(tag,html_nodes)
    return block_parent

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    for block in blocks:
        block_type = block_to_block_type(block)
        #print(f"This {block}")
        match block_type:
            case BlockType.HEADING:
                text,tag = which_heading(block)
                block_parent = block_to_parent(text, tag)
            case BlockType.CODE:
                text = replace_markdown(block, "```")
                html_node = LeafNode(text, "code")
                block_parent = ParentNode("pre", [html_node])
            case BlockType.QUOTE:
                text = replace_markdown(block, ">")
                block_parent = block_to_parent(text, "blockquote")
            case BlockType.UNORDERED_LIST:
                text = replace_markdown(block, '-')
                html_nodes = make_list_items(text.split("\n"))
                block_parent = ParentNode("ul", html_nodes)
            case BlockType.ORDERED_LIST:
                html_nodes = remove_number_and_period(block)
                block_parent = ParentNode("ol", html_nodes)
            case _:
                block_parent = block_to_parent(block, "p")
        result.append(block_parent)
    div_parent = ParentNode("div", result)
    return div_parent

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if "# " == line[:2]:
            return line[2:]
