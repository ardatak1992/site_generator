from textnode import *
from htmlnode import *


def main():
  node = TextNode("`code block` word this is `code a`", TextType.TEXT)
  new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
  print(new_nodes)

if __name__ == "__main__":
  main()
