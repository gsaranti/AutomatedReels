# Script to create images with numbers centered on them.
# These images can then be used to train models.

from PIL import Image, ImageDraw, ImageFont
import os

# Output directory
output_dir = "number_images"
os.makedirs(output_dir, exist_ok=True)

# Font settings
font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"  # Update path if needed
font_sizes = [12, 24, 36, 48, 60]  # Font sizes

# Background colors (Earth tones + black)
earth_tones = [
    (19, 79, 19),   # Darker Forest Green
    (53, 71, 17),   # Darker Olive Drab
    (69, 34, 9),    # Darker Saddle Brown
    (56, 64, 72),   # Darker Slate Gray
    (35, 65, 90),   # Darker Steel Blue
    (42, 53, 23),   # Darker Dark Olive Green
    (80, 41, 22),   # Darker Sienna
    (24, 39, 39),   # Darker Dark Slate Gray
    (105, 90, 70),  # Darker Tan
    (0, 0, 0)       # Black
]

# Generate images for numbers 0-99
for number in range(100):
    for i, bg_color in enumerate(earth_tones):
        for font_size in font_sizes:
            # Create an image with the background color
            img = Image.new("RGB", (128, 128), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Load font
            try:
                font = ImageFont.truetype(font_path, font_size)
            except OSError:
                font = ImageFont.load_default()

            # Draw the number centered on the image
            text = str(number)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((img.width - text_width) // 2, ((img.height - text_height) // 2) - (text_height / 2))
            draw.text(position, text, font=font, fill=(255, 255, 255))

            # Save the image
            filename = f"{number}_{i}_{font_size}.png"
            img.save(os.path.join(output_dir, filename))

print(f"Images saved in {output_dir}")
