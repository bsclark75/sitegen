import unittest

from blocks import *

class TestFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block - This is a list item - This is another list item",
            ],
            blocks,
        )
    
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_code(self):
        block = """``` def add(a,b):
        sum = a + b
        return sum```"""
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_unorderlist(self):
        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_orderlist(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_headings(self):
        md = """
# This is a headings 1

## This is a headings 2

### This is a headings 3

#### This is a headings 4

##### This is a headings 5

###### This is a headings 6
"""

        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        #print(html)
        self.assertEqual(
        html,
        "<div><h1> This is a headings 1</h1><h2> This is a headings 2</h2><h3> This is a headings 3</h3><h4> This is a headings 4</h4><h5> This is a headings 5</h5><h6> This is a headings 6</h6></div>",
    )

    def test_quotes(self):
        md = """
> This is a quote block.

> This is another quote block.
"""

        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        #print(html)
        self.assertEqual(
        html,
        "<div><blockquote> This is a quote block.</blockquote><blockquote> This is another quote block.</blockquote></div>",
    )

    def test_orderedlist(self):
        md = """
1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""


        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        #print(html)
        self.assertEqual(
        html,
        "<div><ol><li>This is the first list item in a list block </li><li>This is a list item </li><li>This is another list item</li></ol></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code> This is text that _should_ remain the **same** even with inline stuff </code></pre></div>",
        )
    def test_extract_title(self):
        md = """
# This is a headings 1

## This is a headings 2

### This is a headings 3

#### This is a headings 4

##### This is a headings 5

###### This is a headings 6
"""
        text = extract_title(md)
        self.assertEqual("This is a headings 1", text)