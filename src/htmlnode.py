class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    return ' '.join(f'{k}="{v}"' for k, v in self.props.items())

  def __repr__(self):
    return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value == None:
      raise ValueError("Leaft node should have a value")
    if self.tag == None:
      return self.value
    
    return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag == None:
      raise ValueError("Parent node should have a tag")
    if self.children == None:
      raise ValueError("Parent node should have children")
    
    inner_str = ""

    for child in self.children:
      inner_str += child.to_html()

    return f"<{self.tag}>{inner_str}</{self.tag}>"
    







