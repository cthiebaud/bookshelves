from collections import namedtuple
from PIL import Image, ImageDraw

Colors = namedtuple('Colors', ['black', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white'])

def lerp(start, end, t):
    return tuple(int(start[i] + t * (end[i] - start[i])) for i in range(3))

def create_gradient_face(width, height, colors):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            t_x = x / width
            t_y = y / height

            top_color = lerp(colors[0], colors[1], t_x)
            bottom_color = lerp(colors[2], colors[3], t_x)
            pixel_color = lerp(top_color, bottom_color, t_y)

            draw.point((x, y), fill=pixel_color)

    return image

def main():
    width, height = 256, 256

    colors = Colors(
        black=(0, 0, 0),
        red=(255, 0, 0),
        green=(0, 255, 0),
        blue=(0, 0, 255),
        yellow=(255, 255, 0),
        magenta=(255, 0, 255),
        cyan=(0, 255, 255),
        white=(255, 255, 255),
    )

    combinations = [
        (colors.green, colors.black, colors.yellow, colors.red),
    ]

    for i, combination in enumerate(combinations):
        image = create_gradient_face(width, height, combination)
        image.save(f"gradient_face_{i + 1}.png")

if __name__ == "__main__":
    main()
