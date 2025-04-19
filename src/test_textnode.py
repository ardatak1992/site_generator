import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.BOLD, "http://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD,  "http://test.com")
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.LINK, "http://test.com" )
        node2 = TextNode("This is a text node", TextType.LINK, "http://test.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is **bold** and this `a code` and this _`italic code`_.", TextType.TEXT)
        node2 = TextNode("Bold node", TextType.BOLD)
        node3 = TextNode("This is `code from` second node", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node,node2, node3], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is **bold** and this ", TextType.TEXT),
            TextNode("a code", TextType.CODE),
            TextNode(" and this _", TextType.TEXT),
            TextNode("italic code", TextType.CODE),
            TextNode("_.", TextType.TEXT),
            TextNode("Bold node", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("code from", TextType.CODE),
            TextNode(" second node", TextType.TEXT)
        ], split_nodes )


if __name__ == "__main__":
    unittest.main()
