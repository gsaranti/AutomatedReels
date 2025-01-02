import os
import cv2
import numpy as np

# value_min = 200 # DEFAULT
# saturation_max = 50  # DEFAULT

# value_min = 150  # Include less bright pixels
# saturation_max = 100  # Allow slightly more saturated colors

def isolate_white(image_path, value_min=200, saturation_max=50):
    """
    Processes the image to replace all pixels except those that are white.

    Parameters:
    - image_path: Path to the input image.
    - value_min: Minimum brightness (value) for a pixel to be considered white.
    - saturation_max: Maximum saturation for a pixel to be considered white.

    Returns:
    - result: The processed image as a NumPy array with only white pixels retained.
    """
    # Load the image
    image = cv2.imread(image_path)

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define thresholds for white
    lower_white = np.array([0, 0, value_min])  # Minimum value and low saturation
    upper_white = np.array([180, saturation_max, 255])  # Maximum value and saturation

    # Create a mask for white pixels
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=white_mask)

    # Replace all non-white pixels with black
    result[white_mask == 0] = [0, 0, 0]

    return result

def process_images(input_dir, output_dir, value_min=125, saturation_max=50):
    """
    Processes all images in a directory to isolate white pixels and saves the results in the same file format.

    Parameters:
    - input_dir: Path to the directory containing input images.
    - output_dir: Path to the directory where processed images will be saved.
    - value_min: Minimum brightness (value) for a pixel to be considered white.
    - saturation_max: Maximum saturation for a pixel to be considered white.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        # Check for image file extensions
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            input_path = os.path.join(input_dir, file_name)

            # Keep the original file extension
            file_base, file_ext = os.path.splitext(file_name)
            output_path = os.path.join(output_dir, f"{file_base}_isolated{file_ext}")

            # Process the image
            processed_image = isolate_white(input_path, value_min, saturation_max)

            # Save the processed image in the same format
            cv2.imwrite(output_path, processed_image)
            print(f"Processed and saved: {output_path}")

# Example usage
input_directory = "../../../../../../../Desktop/final_fortnite_yolov8_dataset/train/images"  # Replace with your input directory path
output_directory = "../../../../../../../Desktop/final_fortnite_yolov8_dataset/train/iso_images"  # Replace with your output directory path
process_images(input_directory, output_directory)
