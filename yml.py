import colorsys
import glob
import io
import json
import os
import sys
import webcolors
import yaml
    
from pathlib import PurePath 
from colorthief import ColorThief

def concatExcludeLast(strlst):
    return '/'.join(strlst[0:-1])

try:
    os.remove('everything.yaml')
except OSError:
    pass

# root_dir needs a trailing slash (i.e. /root/dir/)
i = 0
my_dictionary = {}
for filename in glob.iglob('**/*.yaml', recursive=True):
    # print("-------------")
    print(i, os.path.basename(filename))
    parts = PurePath(filename).parts
    house = parts[0]
    folder = parts[len(parts) - 2]
    where = '/' + concatExcludeLast(parts)

    # if not 'enfer' in filename:

    with open(filename, 'r') as f:
        if os.fstat(f.fileno()).st_size != 0: # https://stackoverflow.com/a/283719/1070215
            data = yaml.safe_load(f)
            for key, value in data.items():
                value["where"] = where
                tags = value.get("tags", [])
                tags.append(folder)
                tags.append(house)
                tags.append(value["lan"])
                value["tags"] = tags
            my_dictionary.update(data)
    
    i = i + 1

images = []
extensions = ['jpg', 'jpeg', 'webp', 'png']

def classify(hue, lgt, sat):
    if (lgt < 0.1):
        return "black"
    if (lgt > 0.9):
        return "white"
    if (sat < 0.2):
        return "gray"
    if (hue < 30/360.0)   :
        return "red"
    if (hue < 90/360.0)   :
        return "yellow"
    if (hue < 150/360.0)  :
        return "green"
    if (hue < 210/360.0)  :
        return "cyan"
    if (hue < 270/360.0)  :
        return "blue"
    if (hue < 330/360.0)  :
        return "magenta"
    return "red"

i = 0
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('thumbs/*.'+ext, recursive=True):

      # if not 'enfer' in filename2:
      
        # print(os.path.basename(filename2))
        key = PurePath(filename2).stem[2:]
        images.append(filename2)
        my_dictionary[key]["image_path"] = f"thumbs/{os.path.basename(filename2)}" # filename2

        args = len(sys.argv) - 1
        if args > 0:
            color_thief = ColorThief(filename2)
            # get the dominant color
            dominant_color = color_thief.get_color(quality=1)
            r,g,b = dominant_color
            dominant_color_string = f"rgb({r}, {g}, {b})"
            my_dictionary[key]["dominant_color"] = dominant_color_string
            h,l,s = colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0)
            clazz = classify(h,l,s)
            print(i, key, filename2,"-",  r,g,b, "-", h,l,s, "-", clazz)

            tags = my_dictionary[key].get("tags", [])
            tags.append(clazz)
            value["tags"] = tags

        i = i + 1



## print("^^^^^^^^^^^^^^^^^^^^")
## j = 0
## for key, value in my_dictionary.items():
##     if not "image_path" in value:
##         print(j, value)
##         j = j + 1
## print("vvvvvvvvvvvvvvvvvvvv")

with io.open('everything.yaml', 'w',encoding='utf8') as file:
    yaml.dump(my_dictionary, file)

with io.open('images.json', 'w',encoding='utf8') as file2:
    json.dump(images, file2, indent=2)


print(len(my_dictionary))
