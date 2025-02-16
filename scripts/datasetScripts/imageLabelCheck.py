"""
This script confirms that a YOLO dataset has a label file for each image.

Parameters:
  - image_dir: Path to dataset images directory.
  - label_dir: Path to dataset labels directory.
"""

import os

image_dir = ""
label_dir = ""

# List to store image files without matching label files
missing_labels = []

# Process images and check for corresponding label files
for image_file in os.listdir(image_dir):
    if image_file.endswith(('.jpg', '.png', '.jpeg')):  # Add more extensions if needed
        # Get the base name without extension
        base_name = os.path.splitext(image_file)[0]
        # Construct the corresponding label file path
        label_file = os.path.join(label_dir, base_name + ".txt")

        # Check if the label file exists
        if not os.path.exists(label_file):
            missing_labels.append(image_file)

# Log missing label files
if missing_labels:
    print("The following images do not have corresponding label files:")
    for image in missing_labels:
        print(image)
else:
    print("All images have corresponding label files!")
