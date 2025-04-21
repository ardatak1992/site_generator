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
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )

    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev")
        ],
        new_nodes   
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

if __name__ == "__main__":
    unittest.main()
