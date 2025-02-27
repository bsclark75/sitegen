import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_repr(self):
		new_dict = { "href": "https://www.google.com", "target": "_blank", }
		node2 = HTMLNode("p", "This is a text node", None, new_dict)
		self.assertEqual(repr(node2), "HTMLNode(p,This is a text node,,{'href': 'https://www.google.com', 'target': '_blank'})")

	def test_props_to_html(self):
		node2 = HTMLNode("p", "This is a text node", None, {"href": "https://www.microsoft.com", "target": "_blank", })
		self.assertEqual(node2.props_to_html(), " href='https://www.microsoft.com' target='_blank'")

	def test_repr_with_children(self):
		node = HTMLNode("p", "This is a child text node", None, { "href": "https://www.internetplace.net", "target": "_blank", })
		node2 = HTMLNode("p", "This is a parent text node", node, { "href": "https://www.briansclark.net", "target": "_blank", })
		self.assertEqual(repr(node2), "HTMLNode(p,This is a parent text node,HTMLNode(p,This is a child text node,,{'href': 'https://www.internetplace.net', 'target': '_blank'}),{'href': 'https://www.briansclark.net', 'target': '_blank'})")

if __name__ == "__main__":
    unittest.main()
