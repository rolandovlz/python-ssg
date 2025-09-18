import os
import shutil
from textnode import TextNode, TextType

def main():
    # node = TextNode("This is some anchor text", TextType.LINK, "https://rvelez.dev")
    # print(node)
    generate_public()

def generate_public(src=None, dest=None):
    project_root = os.path.dirname(os.path.dirname(__file__))
    public_path = os.path.join(project_root, "public")

    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    copy_dir_files(os.path.join(project_root, "static"), public_path)


def copy_dir_files(src_dir, dest_dir=None):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dest_item = os.path.join(dest_dir, item)
        if os.path.isdir(src_item):
            copy_dir_files(src_item, dest_item)
        else:
            shutil.copy(src_item, dest_item)

main()