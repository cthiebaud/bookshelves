from collections import namedtuple
from PIL import Image, ImageDraw

ColorInfo = namedtuple('ColorInfo', ['rgb', 'name'])

def lerp(start, end, t):
    return tuple(int(start[i] + t * (end[i] - start[i])) for i in range(3))

def create_gradient_face(width, height, colors):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            t_x = x / width
            t_y = y / height

            top_color = lerp(colors[0].rgb, colors[1].rgb, t_x)
            bottom_color = lerp(colors[3].rgb, colors[2].rgb, t_x)
            pixel_color = lerp(top_color, bottom_color, t_y)

            draw.point((x, y), fill=pixel_color)

    return image

def save_image_with_color_names(image, colors):
    color_names = '_'.join([color.name.lower() for color in colors])
    filename = f"gradient_{color_names}.png"
    image.save(filename)

def main():
    width, height = 256, 256

    color_dict = {
        'black': ColorInfo(rgb=(0, 0, 0), name='black'),
        'red': ColorInfo(rgb=(255, 0, 0), name='red'),
        'green': ColorInfo(rgb=(0, 255, 0), name='green'),
        'blue': ColorInfo(rgb=(0, 0, 255), name='blue'),
        'yellow': ColorInfo(rgb=(255, 255, 0), name='yellow'),
        'magenta': ColorInfo(rgb=(255, 0, 255), name='magenta'),
        'cyan': ColorInfo(rgb=(0, 255, 255), name='cyan'),
        'white': ColorInfo(rgb=(255, 255, 255), name='white'),
    }

    combinations = [
        (color_dict['green'], color_dict['black'], color_dict['red'], color_dict['yellow']),
        (color_dict['cyan'], color_dict['blue'], color_dict['black'], color_dict['green']),
        (color_dict['white'], color_dict['magenta'], color_dict['blue'], color_dict['cyan']),
        (color_dict['yellow'], color_dict['red'], color_dict['magenta'], color_dict['white']),

        (color_dict['yellow'], color_dict['green'], color_dict['cyan'], color_dict['white']),

        (color_dict['red'], color_dict['black'], color_dict['blue'], color_dict['magenta']),
        # Add more combinations as needed
    ]

    for i, combination in enumerate(combinations):
        image = create_gradient_face(width, height, combination)
        save_image_with_color_names(image, combination)

if __name__ == "__main__":
    main()
