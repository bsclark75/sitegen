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
        block = block.replace('\n', ' ')
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

def make_children_nodes(nodes, tag=None):
    html_nodes = []
    if tag == None:
        for node in nodes:
            html_nodes.append(text_node_to_html_node(node))
    else:
        for node in nodes:
            html_nodes.append(LeafNode(node.text, tag))
    return html_nodes

def replace_markdown(markdown, text):
    return markdown.replace(text, "")

def which_heading(block):
    if "######" in block:
        text = replace_markdown(block, "######")
        html_node = LeafNode(text, "h6")
    elif "#####" in block:
        text = replace_markdown(block, "#####")
        html_node = LeafNode(text, "h5")
    elif "####" in block:
        text = replace_markdown(block, "####")
        html_node = LeafNode(text, "h4")
    elif "###" in block:
        text = replace_markdown(block, "###")
        html_node = LeafNode(text, "h3")
    elif "##" in block:
        text = replace_markdown(block, "##")
        html_node = LeafNode(text, "h2")
    else:
        text = replace_markdown(block, "#")
        html_node = LeafNode(text, "h1")
    return html_node

def make_list_items(items):
    result = []
    for item in items:
        if item != "":
            result.append(LeafNode(item, "li"))
    return result

def remove_number_and_period(string):
    list_items = re.findall(r'\d+\.\s*[^0-9]+', string)
    cleaned_list_items = [re.sub(r'^\d+\.\s*', '', item) for item in list_items]
    return cleaned_list_items

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []
    is_a_parent = False
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                html_node = which_heading(block)
            case BlockType.CODE:
                is_a_parent = True
                text = replace_markdown(block, "```")
                html_node = LeafNode(text, "code")
                block_parent = ParentNode("pre", [html_node])
            case BlockType.QUOTE:
                text = replace_markdown(block, ">")
                html_node = LeafNode(text, "blockquote")
            case BlockType.UNORDERED_LIST:
                is_a_parent = True
                list_items = block.split('-')
                #print(list_items)
                children = make_list_items(list_items)
                #print(children)
                block_parent = ParentNode("ul", children)
            case BlockType.ORDERED_LIST:
                is_a_parent = True
                list_items = remove_number_and_period(block)
                children = make_list_items(list_items)
                block_parent = ParentNode("ol", children)
            case _:
                is_a_parent = True
                nodes = text_to_textnodes(block)
                html_nodes = make_children_nodes(nodes)
                block_parent = ParentNode("p",html_nodes)
        if is_a_parent == True:
            result.append(block_parent)
        else:
            result.append(html_node)
    div_parent = ParentNode("div", result)
    return div_parent
