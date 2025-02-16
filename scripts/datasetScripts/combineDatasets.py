"""
This script combines multiple YOLO dataset directories into a single dataset.

Parameters:
  - input_dirs: List of paths to the input YOLO dataset directories.
  - output_dir: Path to the output YOLO dataset directory.
"""

import os
import shutil

input_directories = [
    "",  # Replace with paths to your input YOLO datasets
    "",
    "",
    ""
]
output_directory = ""  # Replace with the path to the output dataset


def combine_yolo_datasets(input_dirs, output_dir):
    # Define subdirectories to combine
    subdirs = [
        "train/images",
        "train/labels",
        "val/images",
        "val/labels"
    ]

    # Ensure the output directory structure exists
    for subdir in subdirs:
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)

    # Combine files from each input directory
    for input_dir in input_dirs:
        for subdir in subdirs:
            input_subdir = os.path.join(input_dir, subdir)
            output_subdir = os.path.join(output_dir, subdir)

            if os.path.exists(input_subdir):
                for file_name in os.listdir(input_subdir):
                    input_file = os.path.join(input_subdir, file_name)
                    output_file = os.path.join(output_subdir, file_name)

                    # Avoid overwriting files with the same name by renaming them
                    if os.path.exists(output_file):
                        base_name, ext = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(output_file):
                            output_file = os.path.join(output_subdir, f"{base_name}_{counter}{ext}")
                            counter += 1

                    # Copy the file to the output directory
                    shutil.copy(input_file, output_file)
                    print(f"Copied: {input_file} -> {output_file}")

    print("Dataset combination complete.")


combine_yolo_datasets(input_directories, output_directory)
