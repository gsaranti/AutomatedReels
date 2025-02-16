"""
This script visualizes a YOLO dataset. It should be used to validate that the label data is accurate
so that bounding boxes are correctly set.

Parameters:
  - images_dir: Path to dataset images directory.
  - labels_dir: Path to dataset labels directory.
  - class_names: List of the dataset class names
"""

import cv2
import os

images_dir = ''
labels_dir = ''
class_names = ["eliminated", "knocked", "victory_royale"]  # Update with your class names

# Iterate over images
for image_file in os.listdir(images_dir):
    if image_file.endswith(('.jpg', '.png')):  # Process image files only
        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, os.path.splitext(image_file)[0] + '.txt')

        # Load the image
        image = cv2.imread(image_path)

        # Read and parse label file
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:  # Skip empty lines
                    continue

                parts = line.split()
                if len(parts) != 5:  # Skip malformed lines
                    print(f"Skipping malformed line in {label_path}: {line}")
                    continue

                # Unpack label values
                class_id, x_center, y_center, width, height = map(float, parts)
                class_id = int(class_id)

                # Convert YOLO format to bounding box coordinates
                img_h, img_w, _ = image.shape
                x_center, y_center = x_center * img_w, y_center * img_h
                width, height = width * img_w, height * img_h
                x_min, y_min = int(x_center - width / 2), int(y_center - height / 2)
                x_max, y_max = int(x_center + width / 2), int(y_center + height / 2)

                # Draw the bounding box
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                label = class_names[class_id] if class_names else str(class_id)
                cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the image
        cv2.imshow('Image with Bounding Boxes', image)

        # Wait for key press
        key = cv2.waitKey(0)  # Wait indefinitely for a key press
        if key == ord('q'):  # Exit if 'q' is pressed
            print("Exiting visualization.")
            break

# Clean up OpenCV windows
cv2.destroyAllWindows()
