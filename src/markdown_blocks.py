from enum import Enum
from htmlnode import *
from textnode import *
import re
from inline_markdown import text_to_textnodes

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text):
  
  result_blocks = []
  blocks = text.split("\n\n")

  for block in blocks:
    new_block = block.strip()
    if len(new_block) > 0:
      result_blocks.append(new_block)
  
  return result_blocks


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
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)

  return ParentNode("div", children, None)


def block_to_html_node(block):
  block_type = block_to_block_type(block)
  match block_type:
    case BlockType.PARAGRAPH:
      return paragraph_to_html_node(block)
    case BlockType.HEADING:
      return heading_to_html_node(block)
    case BlockType.CODE:
      return code_to_html_node(block)
    case BlockType.ORDERED_LIST:
      return olist_to_html_node(block)
    case BlockType.UNORDERED_LIST:
      return ulist_to_html_node(block)
    case BlockType.QUOTE:
      return quote_to_html_node(block)
    case _:
      raise ValueError("invalid block type")


def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children


def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)


def heading_to_html_node(block):
  level = 0
  for char in block:
    if char == "#":
      level += 1
    else:
      break
  
  if level + 1 >= len(block):
    raise ValueError("invalid heading level: {level}")
  text = block[level + 1:]
  children = text_to_children(text)
  return ParentNode(f"h{level}", children)

def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("invalid code block")  
  text = block[4: -3]
  raw_text_node = TextNode(text, TextType.TEXT)
  child = text_node_to_html_node(raw_text_node)
  code = ParentNode("code", [child])
  return ParentNode("pre", [code])

def olist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[3:]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ol", html_items)

def ulist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[2:]
    children = text_to_children(text)
    html_items.append(ParentNode("li", children))
  return ParentNode("ul", html_items)


def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)
 
