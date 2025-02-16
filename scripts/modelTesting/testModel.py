"""
This script processes all images in a given folder using a YOLO model.

Parameters:
  - FOLDER_PATH: Path to images.
  - MODEL_PATH: Path to model.
"""

import cv2
import os
from ultralytics import YOLO

FOLDER_PATH = ""
MODEL_PATH = "../../models/best_isolated.pt"


def process_images(folder_path, model):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print("No image files found in the specified folder.")
        return

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read {image_file}. Skipping...")
            continue

        # Run inference
        results = model(image)

        # Use YOLO's built-in rendering to draw bounding boxes
        annotated_image = results[0].plot()

        # Display the image
        cv2.imshow("Detections", annotated_image)

        # Wait for user input
        key = cv2.waitKey(0) & 0xFF

        # Exit early if 'q' is pressed
        if key == ord('q'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()


def main():
    if not os.path.exists(FOLDER_PATH):
        print("The specified folder path does not exist.")
        return

    if not os.path.exists(MODEL_PATH):
        print("The specified model path does not exist. Please check the paths.")
        return

    # Load the YOLO model
    model = YOLO(MODEL_PATH)

    # Process the images
    process_images(FOLDER_PATH, model)


if __name__ == "__main__":
    main()
