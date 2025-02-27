from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(textnode):
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
			return LeafNode(None, "img", {'src':textnode.url, 'alt':textnode.text})
		case _:
			raise ValueError("Unexpected text node")