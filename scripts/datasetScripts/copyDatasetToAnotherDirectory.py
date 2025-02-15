"""
This script copies a dataset to a given directory.

Before running make sure to set the source_folder and destination_folder paths.
"""

import shutil
import os

# Set the source and destination paths
source_folder = ""
destination_folder = ""


def copy_folder(source, destination):
    if os.path.exists(destination):
        print(f"⚠️ Destination folder '{destination}' already exists. Overwriting...")
        shutil.rmtree(destination)  # Remove existing destination folder

    shutil.copytree(source, destination)
    print(f"✅ Successfully copied '{source}' to '{destination}'")


# Run the copy function
copy_folder(source_folder, destination_folder)
