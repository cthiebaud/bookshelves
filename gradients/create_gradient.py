from PIL import Image

def lerp_color(start, end, t):
    """
    Linear interpolation between two RGB colors.
    """
    return tuple(int(start_channel + t * (end_channel - start_channel)) for start_channel, end_channel in zip(start, end))

def create_gradient_image(width, height, start_color, end_color):
    image = Image.new("RGB", (width, height))
    pixels = []

    # Generate unique RGB colors for each pixel
    for r in range(256):
        for g in range(256):
            for b in range(256):
                pixels.append((r, g, b))

    # Sort the list of pixels based on their distance to the start and end colors
    pixels.sort(key=lambda rgb: sum(abs(c1 - c2) for c1, c2 in zip(rgb, start_color)) + sum(abs(c1 - c2) for c1, c2 in zip(rgb, end_color)))

    # Assign each pixel its unique RGB color
    for x in range(width):
        for y in range(height):
            pixel_index = y * width + x
            t = pixel_index / (width * height - 1)  # Normalized value between 0 and 1
            lerped_color = lerp_color(start_color, end_color, t)
            image.putpixel((x, y), lerped_color)

    return image

# Set the desired dimensions of the image
width = 256
height = 256

# Set the start and end colors (RGB format)
start_color = (255, 0, 0)  # Red
end_color = (0, 0, 255)    # Blue

# Create the gradient image
gradient_image = create_gradient_image(width, height, start_color, end_color)

# Save the image
gradient_image.save("lerp_gradient_image.png")
