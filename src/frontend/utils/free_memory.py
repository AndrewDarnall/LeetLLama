""" Remove All Previously Uploaded Files to Avoid Saturation of Container Memory """
from os import (
    remove as os_remove,
    walk as os_walk
)
from os.path import join as os_join

def remove_all_files_in_dir(root_dir="/app/.files/"):
    for dirpath, dirnames, filenames in os_walk(root_dir):
        for filename in filenames:
            file_path = os_join(dirpath, filename)
            try:
                os_remove(file_path)
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to delete {file_path}: {e}")