from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def text_node_to_html_node(textnode):
    #print(f"TEXTNODE: {textnode}")
    match textnode.text_type:
           case TextType.NORMAL:
            return LeafNode(textnode.text)
           case TextType.BOLD:
            return LeafNode(textnode.text, "b")
           case TextType.ITALIC:
            return LeafNode(textnode.text, "i")
           case TextType.CODE:
            return LeafNode(textnode.text, "code")
           case TextType.LINKS:
            return LeafNode(textnode.text, "a", {'href': textnode.url })
           case TextType.IMAGES:
            return LeafNode(textnode.text, "img", {'src':textnode.url, 'alt':textnode.text})
           case _:
            raise ValueError("Unexpected text node")
		
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    print(f"OLD NODES: {old_nodes}, DELIMITER: {delimiter}, TEXT_TYPE: {text_type}")
    if isinstance(old_nodes, str):
        old_nodes = [TextNode(old_nodes, TextType.NORMAL)]
        
    # If text_type is NORMAL, just add all nodes as they are
    if text_type == TextType.NORMAL:
        new_nodes.extend([TextNode(node.text, text_type, node.url) for node in old_nodes])
        return new_nodes

    # Iterate over each node in old_nodes
    for old_node in old_nodes:
        count = 0
        # If the node's text_type is not NORMAL, extend the new nodes list with the old node itself
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)  # Append the whole old node directly
            continue  # Skip to the next node

        # Split the old node's text by the delimiter
        split_up_texts = old_node.text.split(delimiter)

        # Process each part of the split text
        for text in split_up_texts:
            if count % 2 == 0:
                # Even index parts are added with the old node's text_type
                new_nodes.append(TextNode(text, old_node.text_type, old_node.url))
            else:
                # Odd index parts are added with the new text_type
                new_nodes.append(TextNode(text, text_type, old_node.url))
            count += 1

    return new_nodes


def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def split_nodes_link(nodes):
    result = []
    link_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\)]+)\)')

    for node in nodes:
        text = node.text
        start_idx = 0
        
        if not link_pattern.search(text):
            result.append(node)
            continue

        for match in link_pattern.finditer(text):
            result.append(TextNode(text[start_idx:match.start()], TextType.NORMAL))
            link_text, url = match.groups()
            result.append(TextNode(link_text, TextType.LINKS, url))
            start_idx = match.end()
        if start_idx < len(text):
            result.append(TextNode(text[start_idx:], TextType.NORMAL))
    
    return result

def split_nodes_image(nodes):
    #print("start node image")
    result = []
    # Updated regex pattern to match image markdown: ![alt_text](url)
    image_pattern = re.compile(r'!\[([^\]]+)\]\(((?!https?://)[^\)]+)\)')

    for node in nodes:
        text = node.text
        start_idx = 0
        
        # If no image pattern matches, skip this node
        if not image_pattern.search(text):
            #print("Pattern not found")
            result.append(node)
            continue

        # Find all matches for images in the text
        for match in image_pattern.finditer(text):
            # Add the part of the text before the image as a TEXT node
            result.append(TextNode(text[start_idx:match.start()], TextType.NORMAL))
            
            # Add the image part as an IMAGE node (capturing only the alt text and URL)
            image_text, url = match.groups()
            result.append(TextNode(image_text, TextType.IMAGES, url))
            
            # Update start index to be the end of the current match
            start_idx = match.end()
        
        # Add the remaining part of the text as a TEXT node
        if start_idx < len(text):
            result.append(TextNode(text[start_idx:], TextType.NORMAL))
    
    return result


def text_to_textnodes(text):
      new_nodes = split_nodes_delimiter(text,None,TextType.NORMAL)
      new_nodes = split_nodes_delimiter(new_nodes,'**', TextType.BOLD)
      new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
      new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
      new_nodes = split_nodes_image(new_nodes)
      #print(new_nodes)
      new_nodes = split_nodes_link(new_nodes)
      return new_nodes