"""
This script checks that the label folders within two different datasets have the same file names and content.
For example, it compares the /train/labels file names of two different datasets.

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


def get_file_mapping(folder, allow_postfix=False):
    file_mapping = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):  # Ensure only .txt files are considered
            name, ext = os.path.splitext(filename)
            base_name = name[:-len(postfix)] if allow_postfix and name.endswith(postfix) else name
            file_mapping[base_name] = os.path.join(folder, filename)
    return file_mapping


def compare_file_contents(file1, file2):
    """Compares the contents of two text files."""
    with open(file1, 'r', encoding="utf-8") as f1, open(file2, 'r', encoding="utf-8") as f2:
        return f1.read() == f2.read()


def compare_folders():
    files1 = get_file_mapping(folder1, allow_postfix=False)
    files2 = get_file_mapping(folder2, allow_postfix=True)

    # Compare filenames
    missing_in_folder2 = set(files1.keys()) - set(files2.keys())
    extra_in_folder2 = set(files2.keys()) - set(files1.keys())

    if missing_in_folder2:
        print(f"❌ Missing files in folder2: {missing_in_folder2}")
    if extra_in_folder2:
        print(f"❌ Extra files in folder2 (unexpected without base match): {extra_in_folder2}")

    # Compare file contents
    mismatched_files = []
    for base_name in files1.keys() & files2.keys():
        if not compare_file_contents(files1[base_name], files2[base_name]):
            mismatched_files.append(base_name)

    if mismatched_files:
        print(f"⚠️ Content mismatch in files: {mismatched_files}")
    else:
        print("✅ All filenames and file contents match.")


# Run the comparison
compare_folders()
