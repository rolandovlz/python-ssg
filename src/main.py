import os
import shutil
import sys

from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(basepath)

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_dir_files(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


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