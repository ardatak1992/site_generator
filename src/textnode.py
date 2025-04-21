import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"


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

def extract_markdown_images(text):
  matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches

def extract_markdown_links(text):
  matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches


def split_nodes_image(old_nodes):
  all_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      all_nodes.append(old_node)
      continue 

    old_node_text = old_node.text
    new_nodes = []
    matches = extract_markdown_images(old_node_text)

    if len(matches) == 0:
      all_nodes.append(old_node)
      continue

    for match in matches:
      (image_alt, image_link) = match
      sections = old_node_text.split(f"![{image_alt}]({image_link})", 1)
      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
      new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
     
      old_node_text = "".join(sections[1:])
    all_nodes.extend(new_nodes)
    if len(old_node_text) != 0:
      all_nodes.append(TextNode(old_node_text, TextType.TEXT))
  return all_nodes


def split_nodes_link(old_nodes):
  all_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      all_nodes.append(old_node)
      continue 

    old_node_text = old_node.text
    new_nodes = []
    matches = extract_markdown_links(old_node_text)

    if len(matches) == 0:
      all_nodes.append(old_node)
      continue

    for match in matches:
      (image_alt, image_link) = match
      sections = old_node_text.split(f"[{image_alt}]({image_link})", 1)
      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
      old_node_text = "".join(sections[1:])
    all_nodes.extend(new_nodes)
    if len(old_node_text) != 0:
      all_nodes.append(TextNode(old_node_text, TextType.TEXT))
  return all_nodes


def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
  nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)

  
  return nodes


def markdown_to_blocks(text):
  blocks = text.split("\n\n")
  blocks = list(map(lambda x: x.strip(), blocks))
  return blocks

def block_to_block_type(text):
  heading_regex = re.compile(r"#{1,6} ")
  code_regex = re.compile(r"^```([^\[\]]*)```$", re.MULTILINE)
  quote_regex = re.compile(r"^>")
  ul_regex = re.compile(r"^- ")
  ol_regex = re.compile(r"^\d+. ")


  if heading_regex.match(text):
    return BlockType.HEADING
  if code_regex.match(text):
    return BlockType.CODE
  if quote_regex.match(text):
    return BlockType.QUOTE
  if ul_regex.match(text):
    return BlockType.UNORDERED_LIST
  if ol_regex.match(text):
    return BlockType.ORDERED_LIST
  
  return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  
