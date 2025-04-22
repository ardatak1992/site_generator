import unittest
from htmlnode import *
from inline_markdown import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is a link", [], {"href": "test.com", "target": "_blank"})
        nodeProps = node.props_to_html()
        self.assertEqual(nodeProps, 'href="test.com" target="_blank"')
        self.assertEqual(node.__repr__(), f"HTMLNode(tag={node.tag}, value={node.value}, children={node.children}, props={node.props})")
    def test_leaf_to_html_p(self):
      node = LeafNode("p", "Hello, world!")
      self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
      node = LeafNode("a", "This is a link")
      self.assertEqual(node.to_html(), "<a>This is a link</a>")
    def test_leaf_to_html_b(self):
      node = LeafNode("b", "Hello, world in bold")
      self.assertEqual(node.to_html(), "<b>Hello, world in bold</b>")
    def test_left_to_raw_text(self):
      node = LeafNode(None, "Just text")
      self.assertEqual(node.to_html(), "Just text")
    def test_to_html_with_children(self):
      child_node = LeafNode("span", "child")
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
      grandchild_node = LeafNode("b", "grandchild")
      child_node = ParentNode("span", [grandchild_node])
      parent_node = ParentNode("div", [child_node])
      self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
      )

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
        

if __name__ == "__main__":
    unittest.main()
