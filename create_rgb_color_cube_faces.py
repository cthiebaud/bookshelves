from PIL import Image, ImageDraw

def create_gradient_image(width, height, start_color, end_color, direction):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for i in range(height):
        r = int(start_color[0] + (i / height) * (end_color[0] - start_color[0]))
        g = int(start_color[1] + (i / height) * (end_color[1] - start_color[1]))
        b = int(start_color[2] + (i / height) * (end_color[2] - start_color[2]))

        if direction == 'horizontal':
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        elif direction == 'vertical':
            draw.line([(i, 0), (i, height)], fill=(r, g, b))

    return image

def main():
    width, height = 256, 256
    colors = [
        ((255, 0, 0), (255, 255, 0)),  # Red to Yellow (Top Face)
        ((0, 255, 0), (255, 255, 0)),  # Green to Yellow (Front Face)
        ((0, 0, 255), (255, 0, 255)),  # Blue to Magenta (Right Face)
        ((255, 255, 0), (255, 0, 0)),  # Yellow to Red (Bottom Face)
        ((0, 255, 255), (0, 255, 0)),  # Cyan to Green (Back Face)
        ((255, 0, 255), (0, 0, 255)),  # Magenta to Blue (Left Face)
    ]

    for i, (start_color, end_color) in enumerate(colors):
        image = create_gradient_image(width, height, start_color, end_color, 'horizontal')
        image.save(f"gradient_face_{i + 1}.png")

if __name__ == "__main__":
    main()
