from htmlnode import *
from textnode import *


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
  
  result_blocks = []
  
  blocks = text.split("\n\n")

  for block in blocks:
    new_block = block.strip()
    

    if len(new_block) > 0:
      result_blocks.append(new_block)
  
  return result_blocks

def get_heading(block):
  if block.startswith("# "):
    return ParentNode("h1", [])
  elif block.startswith("## "):
    return ParentNode("h2", [])
  elif block.startswith("### "):
    return ParentNode("h3", [])
  elif block.startswith("#### "):
    return ParentNode("h4", [])
  elif block.startswith("##### "):
    return ParentNode("h5", [])
  elif block.startswith("###### "):
    return ParentNode("h6", [])

