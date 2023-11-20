from PIL import Image

# Load the images
image_paths = [
    'gradient_cyan_blue_black_green.png',
    'gradient_green_black_red_yellow.png',
    'gradient_red_black_blue_magenta.png',
    'gradient_white_magenta_blue_cyan.png',
    'gradient_yellow_green_cyan_white.png',
    'gradient_yellow_red_magenta_white.png'
]

images = [Image.open(path) for path in image_paths]

# Check if all images have the same dimensions
for i in range(1, len(images)):
    if images[i].size != images[0].size:
        raise ValueError(f"Images {i} and 0 have different dimensions.")

# Create the concatenated image
total_width = images[0].width
total_height = images[0].height
concatenated_image = Image.new('RGB', (total_width, total_height))

# Compress and paste each image in the correct position
left = 0
portion_width = images[0].width // len(images)

for img in images:
    compressed_img = img.resize((portion_width, images[0].height))
    concatenated_image.paste(compressed_img, (left, 0))
    left += portion_width

# Save the result
concatenated_image.save('concatenated_image.png')
