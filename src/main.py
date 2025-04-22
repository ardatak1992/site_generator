import os
import sys
import shutil

from markdown_blocks import markdown_to_html_node


def copy_directory(sourcePath, targetPath):
  
  if not os.path.exists(sourcePath):
    raise FileNotFoundError(f"Directory not found: {sourcePath}")
  
  if os.path.exists(targetPath):
     shutil.rmtree(targetPath)
  if not os.path.exists(targetPath):
    os.mkdir(targetPath)

  directories = os.listdir(sourcePath)
  for directory in directories:
    
    if os.path.isdir(f"{sourcePath}/{directory}"):
      os.mkdir(f"{targetPath}/{directory}")
      copy_directory(f"{sourcePath}/{directory}", f"{targetPath}/{directory}")
    elif not os.path.isfile(directory):
      shutil.copy(f"{sourcePath}/{directory}", targetPath)
    
      
def extract_title(markdown):
  with open(markdown) as f:
    for line in f:
      if line.startswith("# "):
        return line[2:-1]
  raise Exception("Title not found")    
  
def generate_page_recursively(from_path, template_path, dest_path, basepath):

  
  directories = os.listdir(from_path)
  for directory in directories:
    if os.path.isdir(f"{from_path}/{directory}"):
      os.mkdir(f"{dest_path}/{directory}")
      generate_page_recursively(f"{from_path}/{directory}", template_path, f"{dest_path}/{directory}", basepath)
    else:
      generated_html = ""
      html_str = ""
      title = extract_title(f"{from_path}/{directory}")
      
      with open(f"{from_path}/{directory}") as md:
        
        text = md.read()
        html_node = markdown_to_html_node(text)
        generated_html += html_node.to_html()
        

      with open(template_path, "r") as temp:
        html_str += temp.read()
        html_str = html_str.replace(r"{{ Title }}", title)
        html_str = html_str.replace(r"{{ Content }}", generated_html)
        html_str = html_str.replace('href="/', f'href="{basepath}')
        html_str = html_str.replace('src="/', f'src="{basepath}')
        
      with open(f"{dest_path}/index.html", "w+") as f:
        f.write(html_str)


def main():

  basepath = "/"
  if sys.argv[1]:
    basepath = sys.argv[1]

  copy_directory("static", "docs")
  generate_page_recursively("content", "template.html", "docs", basepath)
  
if __name__ == "__main__":
  main()
