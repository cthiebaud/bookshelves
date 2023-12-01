from PIL import Image

def create_rgb_image(width, height):
    image = Image.new("RGB", (width, height))
    pixels = []

    # Generate unique RGB colors for each pixel
    for r in range(256):
        for g in range(256):
            for b in range(256):
                pixels.append((r, g, b))

    # Shuffle the list of pixels to randomize the order
    import random
    random.shuffle(pixels)

    # Assign each pixel its unique RGB color
    for x in range(width):
        for y in range(height):
            pixel_index = y * width + x
            image.putpixel((x, y), pixels[pixel_index])

    return image

# Set the desired dimensions of the image
width = 256
height = 256

# Create the image
result_image = create_rgb_image(width, height)

# Save the image
result_image.save("unique_rgb_image.png")
