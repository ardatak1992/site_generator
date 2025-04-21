from textnode import *
from htmlnode import *


def main():

  md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
  markdown = "``` This is\n code```"
  print(block_to_block_type(markdown))

  

if __name__ == "__main__":
  main()
