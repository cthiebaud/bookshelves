from PIL import Image

# Load the images
image_paths = [
    'gradient_cyan_blue_black_green.png',
    'gradient_blue_magenta_red_black.png',
    'gradient_magenta_white_yellow_red.png',
    'gradient_white_cyan_green_yellow.png',
]
qwe = 'gradient_cyan_white_magenta_blue.png'
asd = 'gradient_black_red_yellow_green.png'

images = [Image.open(path) for path in image_paths]
qweImage = Image.open(qwe)
asdImage = Image.open(asd)

# Check if all images have the same dimensions
for i in range(1, len(images)):
    if images[i].size != images[0].size:
        raise ValueError(f"Images {i} and 0 have different dimensions.")

# Create the concatenated image
total_width = images[0].width * len(images)
total_height = 3*images[0].height
concatenated_image = Image.new('RGB', (total_width, total_height))

# Paste each image in the correct position
left = 0
for img in images:
    concatenated_image.paste(img, (left, images[0].height))
    left += img.width

concatenated_image.paste(qweImage, (images[0].width, 0))
concatenated_image.paste(asdImage, (images[0].width, 2*images[0].height))

# Save the result
concatenated_image.save('concatenated_image0.png')
