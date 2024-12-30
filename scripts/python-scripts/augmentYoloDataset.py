# This script takes a YOLO dataset and creates augmented images and corresponding labels.

import cv2
import os

# Paths
# Directory containing original images
input_dir = "../../fortnite gameplay/Datasets/fortnite_elimination_count_logo_v1_reformat/val/images/"

# Directory containing YOLO labels
label_dir = "../../fortnite gameplay/Datasets/fortnite_elimination_count_logo_v1_reformat/val/labels/"

# Directory to save augmented images
output_dir = "augmented_images"

# Directory to save augmented labels
output_label_dir = "augmented_labels"

# Create output directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

for img_file in os.listdir(input_dir):
    if img_file.endswith(('.jpg', '.png')):
        img_path = os.path.join(input_dir, img_file)
        img = cv2.imread(img_path)
        h, w, _ = img.shape

        # Define the ROI for the top-right quarter of the image
        x_min, y_min = w // 2, 0
        x_max, y_max = w, h // 2

        # Crop the ROI
        cropped = img[y_min:y_max, x_min:x_max]

        # Save cropped image
        aug_img_name = img_file.replace(".jpg", "_right_corner.jpg").replace(".png", "_right_corner.png")
        aug_img_path = os.path.join(output_dir, aug_img_name)
        cv2.imwrite(aug_img_path, cropped)

        # Load corresponding label
        label_path = os.path.join(label_dir, img_file.replace(".jpg", ".txt").replace(".png", ".txt"))
        new_labels = []

        if os.path.exists(label_path):
            with open(label_path, "r") as f:
                lines = f.readlines()

            for line in lines:
                class_id, cx, cy, bw, bh = map(float, line.strip().split())
                cx, cy = cx * w, cy * h  # Convert to absolute coordinates

                if x_min <= cx <= x_max and y_min <= cy <= y_max:
                    # Adjust coordinates relative to the cropped ROI
                    cx = (cx - x_min) / (x_max - x_min)
                    cy = (cy - y_min) / (y_max - y_min)

                    # Scale width and height for the cropped image
                    bw = bw * 2
                    bh = bh * 2

                    new_labels.append(f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

        # Save adjusted labels (empty file if no labels exist)
        aug_label_name = img_file.replace(".jpg", "_right_corner.txt").replace(".png", "_right_corner.txt")
        aug_label_path = os.path.join(output_label_dir, aug_label_name)
        with open(aug_label_path, "w") as f:
            f.write("\n".join(new_labels))

print("Augmentation complete. Cropped images and labels saved.")
