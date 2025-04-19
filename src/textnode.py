from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"


class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, node):
    return self.text == node.text and self.text_type.value == node.text_type.value and self.url == node.url

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
  match text_node.text_type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("b", text_node.text)
    case TextType.IMAGE:
      return LeafNode("img", text_node.text)
    case _:
      raise Exception("invalid text type")
     

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue

    split_text = node.text.split(delimiter)
    if len(split_text) % 2 == 0:
      raise Exception("delimiters not matched")
    line_nodes = []
    for i, text in enumerate(split_text):
      if len(text) > 0:
        if i % 2 == 1:
          line_nodes.append(TextNode(text, text_type))
        else:
          line_nodes.append(TextNode(text, TextType.TEXT))
    new_nodes.extend(line_nodes)

  return new_nodes
