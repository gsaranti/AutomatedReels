"""
This script checks that the same folders within two different datasets have the same file names.
For example, it compares the /train/images file names of two different datasets.

It can also account for if one of the dataset's file names has a postfix. If no postfix is needed,
set to an empty string

Before running make sure to set the folder1 and folder2 paths, as well as the optional postfix value.
IMPORTANT: folder2 should be used for the folder with file names including a postfix.
"""

import os

# Configure your folder paths
folder1 = ""
folder2 = ""  # Folder with postfix if needed
postfix = "_isolated_final"  # Optional


def get_base_filenames(folder, allow_postfix=False):
    base_filenames = set()
    for filename in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, filename)):
            name, ext = os.path.splitext(filename)
            if allow_postfix and name.endswith(postfix):
                name = name[: -len(postfix)]  # Remove postfix
            base_filenames.add(name)
    return base_filenames


def compare_folders():
    files1 = get_base_filenames(folder1, allow_postfix=False)
    files2 = get_base_filenames(folder2, allow_postfix=True)

    # Check if the number of files is the same
    if len(files1) != len(files2):
        print(f"File count mismatch: {len(files1)} files in folder1 vs {len(files2)} in folder2")

    # Compare filenames
    missing_in_folder2 = files1 - files2
    missing_in_folder1 = files2 - files1

    if not missing_in_folder2 and not missing_in_folder1:
        print("✅ All filenames match (accounting for postfix).")
    else:
        if missing_in_folder2:
            print(f"❌ Missing in folder2: {missing_in_folder2}")
        if missing_in_folder1:
            print(f"❌ Extra files in folder2 (unexpected without base match): {missing_in_folder1}")


# Run the comparison
compare_folders()
