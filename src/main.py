import os
import shutil

from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    generate_public()

def generate_public(src=None, dest=None):
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_dir_files(dir_path_static, dir_path_public)

    generate_page(os.path.join(dir_path_content, "index.md"), template_path, os.path.join(dir_path_public, "index.html"))


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