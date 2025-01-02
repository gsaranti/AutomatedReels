# This script takes a YOLO dataset and creates augmented images and corresponding labels.

import cv2
import os

# Paths
# Directory containing original images
input_dir = "../../../../resources/fortnite/Datasets/fortnite_action_text/val/images/"

# Directory containing YOLO labels
label_dir = "../../../../resources/fortnite/Datasets/fortnite_action_text/val/labels/"

# Directory to save augmented images
output_dir = "../../../../resources/fortnite/Datasets/fortnite_action_text/val/augmented_images"

# Directory to save augmented labels
output_label_dir = "../../../../resources/fortnite/Datasets/fortnite_action_text/val/augmented_labels"

# Create output directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

for img_file in os.listdir(input_dir):
    if img_file.endswith(('.jpg', '.png')):
        img_path = os.path.join(input_dir, img_file)
        img = cv2.imread(img_path)
        h, w, _ = img.shape

        # Define the ROI for the middle half of the image (25% padding on left and right sides)
        x_min, y_min = w // 4, 0
        x_max, y_max = 3 * w // 4, h

        # Crop the ROI
        cropped = img[y_min:y_max, x_min:x_max]

        # Save cropped image
        aug_img_name = img_file.replace(".jpg", "_middle_half.jpg").replace(".png", "_middle_half.png")
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

                    # Double the width and keep height the same for YOLO format
                    bw = bw * 2
                    new_labels.append(f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

        # Save adjusted labels (empty file if no labels exist)
        aug_label_name = img_file.replace(".jpg", "_middle_half.txt").replace(".png", "_middle_half.txt")
        aug_label_path = os.path.join(output_label_dir, aug_label_name)
        with open(aug_label_path, "w") as f:
            f.write("\n".join(new_labels))

print("Augmentation complete. Cropped images and labels saved.")
