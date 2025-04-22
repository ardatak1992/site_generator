import unittest
from htmlnode import *
from markdown_blocks import *


class TestMarkdownBlocks(unittest.TestCase):

  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
            blocks,
            [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            ],
    )
        
  def test_block_to_block_type(self):
    blocks = [
            "## Heading",
            "this is a paragraph",
            "### another heading",
            "> quote to quote\n this is a quote",
            "``` This is a code block ```",
            "- unordered list",
            "-this is a parahraph",
            "1. ordered list",
            "1.not an ordered list but paragraph"
        ]

    markdown_types = list(map(lambda x: block_to_block_type(x), blocks))
    self.assertEqual(
            markdown_types,
            [
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.CODE,
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            ],
        )

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
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
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )


if __name__ == "__main__":
    unittest.main()
