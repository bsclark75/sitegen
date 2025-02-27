import unittest
from htmlnode import ParentNode, LeafNode

class TestLeafNode(unittest.TestCase):
	
    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_parent_prop(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node], {"class":"child"})
        self.assertEqual(parent_node.to_html(), "<div class='child'><span>child</span></div>")

    def test_to_html_without_tag(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "No tag provided")

    def test_to_html_without_children(self):
        parent_node = ParentNode("html", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "No children present")
		
if __name__ == "__main__":
    unittest.main()
