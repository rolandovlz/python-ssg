import os
from pathlib import Path
from blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path)
        else:
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(src_path, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    md_content = from_file.read()
    from_file.close()

    template_file =  open(template_path, "r")
    template_content = template_file.read()
    template_file.close()
    
    title = extract_title(md_content)
    nodes = markdown_to_html_node(md_content)
    html = nodes.to_html()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template_content)
