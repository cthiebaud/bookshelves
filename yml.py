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

yellow_threshold = [{
    "lum":255, "sat":1,
    "lum":254, "sat":0.85,
    "lum":253, "sat":0.73,
    "lum":252, "sat":0.63,
    "lum":251, "sat":0.53,
    "lum":250, "sat":0.43,
    "lum":249, "sat":0.33,
    "lum":248, "sat":0.68,
    "lum":248, "sat":0.60,
    
    
}]
def classify(luminance, hue, lgt, sat):

    ## luminance = lgt * 255
    ## r,g,b = dominant_color
    ## hue, lgt, sat = colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0)
    ## if (sat < 0.15) : 
    ##     if (luminance <= 50)   : return "black"
    ##     if (luminance >= 240)   : return "white"
    ##     return "gray"
    ## else:
    ##     if (luminance <= 30)   : return "black"
    ##     if (luminance >= 251)   : return "white"
    ##     ## if (lgt < 0.20)       : return "black"
    ##     ## if (lgt > 0.95)       : return "white"
    ##     ## if (sat < 0.10)       : return "gray"
        
    ## if (sat < 0.1) : 
    ##     if luminance <= 41 :
    ##         return "black"
    ##     if luminance >= 240 :
    ##         return "white"
    ##     return "gray"
    ## else:
        ## 0.05555555555
        if (hue < 20/360.0)     : 
            ## if luminance <= 47  :
            ##     return "black"
            ## if luminance >= 242 :
            ##     return "white"
            ## if sat <= 0.1050    : 
            ##     return "gray"
            return "red"
        # 0.22222222
        if (hue < 80/360.0)   : 
            ## if luminance <= 50:
            ##     return "black"
            ## if luminance >= 245:
            ##     return "white"
            ## if sat <= 0.1050: 
            ##     return "gray"
            return "yellow"
        # 0.3888
        if (hue < 140/360.0)  : 
            ## if luminance <= 41 :
            ##     return "black"
            ## if luminance >= 243 :
            ##     return "white"
            return "green"
        if (hue < 200/360.0)  : 
            ## if luminance <= 41 :
            ##     return "black"
            ## if luminance >= 243 :
            ##     return "white"
            return "cyan"
        if (hue < 260/360.0)  : 
            ##if luminance <= 41 :
            ##    return "black"
            ##if luminance >= 233 :
            ##    return "white"
            return "blue"
        if (hue < 340/360.0)  : 
            ## if luminance <= 41 :
            ##     return "black"
            ## if luminance >= 243 :
            ##     return "white"
            return "magenta"
        ## if luminance <= 47  :
        ##     return "black"
        ## if luminance >= 242 :
        ##     return "white"
        ## if sat <= 0.1050    : 
        ##     return "gray"
        return "red"

# root_dir needs a trailing slash (i.e. /root/dir/)
i = 0
my_dictionary = {}
with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

goodreads = {}

with open('year_first_published.json', 'r') as fp:
    goodreads = json.load(fp)

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
                image_properties = value.get("image_properties", {})
                tags.append(folder)
                tags.append(house)
                tags.append(value["lan"])
                if (key in colors_dictionnary) :
                    hls = colors_dictionnary[key]["hls"]
                    image_properties["hls"] = hls
                    h,l,s = hls.split(", ")                       
                    image_properties["saturation"] = s
                    image_properties["hue"] = h
                    image_properties["lightness"] = l
                    
                    dominant_color = colors_dictionnary[key]["dominant_color"]
                    image_properties["dominant_color"] = dominant_color
                    
                    luminance = colors_dictionnary[key]["luminance"]
                    image_properties["luminance"] = luminance

                    contrast = colors_dictionnary[key]["contrast"]
                    image_properties["contrast"] = contrast

                    monochrome_variance = colors_dictionnary[key]["monochrome_variance"]
                    image_properties["monochrome_variance"] = monochrome_variance
                    if (monochrome_variance < 75):
                        tags.append("rainbow")
                    if True:
                        clazz = classify(luminance, float(h), float(l), float(s))
                        if clazz is not None:
                            tags.append(clazz)
                if key in goodreads:
                    # print("found date", key, goodreads[key])
                    tags.append(f"_{goodreads[key]}")
                value["tags"] = tags
                value["image_properties"] = image_properties
            my_dictionary.update(data)
    
    i = i + 1

images = []
extensions = ['jpg', 'jpeg', 'webp', 'png']

i = 0
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('thumbs/*.'+ext, recursive=True):

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
