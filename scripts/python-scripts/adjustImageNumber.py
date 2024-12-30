# Script for replacing numbers in an image.

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Directory for your existing images and output
input_dir = "start_images"  # Folder containing your original images
output_dir = "image_results"  # Folder to save the updated images
os.makedirs(output_dir, exist_ok=True)

# HUD design
placement_version = "alpha"

# Details on where to find the number and roi for background color
image_details = {
    "alpha": {
        "x_coord": 1814,
        "y_coord": 325,
        "width": 1830,
        "height": 339,
        "roi_coords": (1811, 320, 1830, 325)
    },
    "beta": {
        "x_coord": 1814,
        "y_coord": 17,
        "width": 1830,
        "height": 34,
        "roi_coords": (1811, 0, 1830, 5)
    }
}

# Font settings
font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
font_size = 19

# Background color for number replacement (match HUD style if needed)
text_color = (255, 255, 255)  # White text

# Iterate over images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):  # Support for PNG or JPG
        for replacement_number in range(0, 100):
            # Coordinates for the elimination number box (x, y, width, height)
            x_coord = image_details[placement_version]["x_coord"]
            if replacement_number < 10:
                x_coord = x_coord - 2

            y_coord = image_details[placement_version]["y_coord"]
            width = image_details[placement_version]["width"]
            height = image_details[placement_version]["height"]

            number_box_coords = (x_coord, y_coord, width, height)
            roi_coords = image_details[placement_version]["roi_coords"]

            # Open the image
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)

            # Create a drawing context
            draw = ImageDraw.Draw(img)

            # Determine the background color
            roi = img.crop(roi_coords)
            roi_array = np.array(roi)
            average_color = tuple(roi_array.mean(axis=(0, 1)).astype(int))  # (R, G, B)

            # Clear the area where the number is (draw over with the background color)
            x1, y1, x2, y2 = number_box_coords
            draw.rectangle([x1, y1, x2, y2], fill=average_color)

            # Add the new number
            try:
                font = ImageFont.truetype(font_path, font_size)
            except OSError:
                font = ImageFont.load_default()

            # Calculate position to center the number in the box
            text = str(replacement_number)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_position = (x1, y1 - 5)

            # Draw the new number
            draw.text(text_position, text, font=font, fill=text_color)

            # Save the updated image
            output_path = os.path.join(output_dir, f"updated_{replacement_number}_{filename}")
            img.save(output_path)

            print(f"Updated images saved to {output_dir}")
