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

def classify(luminance, hue, lgt, sat):

    ## r,g,b = dominant_color
    ## hue, lgt, sat = colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0)
    if (sat < 0.18) : 
        if (luminance <= 42)   : return "black"
        if (luminance >= 250)   : return "white"
        return "gray"
    else:
        if (luminance <= 20)   : return "black"
        if (luminance >= 240)   : return "white"
        ## if (lgt < 0.20)       : return "black"
        ## if (lgt > 0.95)       : return "white"
        ## if (sat < 0.10)       : return "gray"
        if (hue < 20/360.0)   : return "red"
        if (hue < 80/360.0)   : return "yellow"
        if (hue < 140/360.0)  : return "green"
        if (hue < 200/360.0)  : return "cyan"
        if (hue < 260/360.0)  : return "blue"
        if (hue < 340/360.0)  : return "magenta"
        return "red"

# root_dir needs a trailing slash (i.e. /root/dir/)
i = 0
my_dictionary = {}
with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

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
                if (key in colors_dictionnary) :
                    hls = colors_dictionnary[key]["hls"]
                    value["hls"] = hls
                    dominant_color = colors_dictionnary[key]["dominant_color"]
                    value["dominant_color"] = dominant_color
                    monochrome_variance = colors_dictionnary[key]["monochrome_variance"]
                    luminance = colors_dictionnary[key]["luminance"]
                    if monochrome_variance > 79:
                        qwe = hls.split(", ")                       
                        clazz = classify(luminance, float(qwe[0]), float(qwe[1]), float(qwe[2]))
                        if clazz is not None:
                            tags.append(clazz)
                value["tags"] = tags
            my_dictionary.update(data)
    
    i = i + 1

images = []
extensions = ['jpg', 'jpeg', 'webp', 'png']

i = 0
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('thumbs/*.'+ext, recursive=True):

      # if not 'enfer' in filename2:
      
        # print(os.path.basename(filename2))
        key = PurePath(filename2).stem[2:]
        images.append(filename2)
        my_dictionary[key]["image_path"] = f"thumbs/{os.path.basename(filename2)}" # filename2

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
