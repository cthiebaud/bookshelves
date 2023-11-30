import glob
import io
import json
import os
import yaml
    
from pathlib import PurePath 

def concatExcludeLast(strlst):
    return '/'.join(strlst[0:-1])

try:
    os.remove('dist/everything.yaml')
except OSError:
    pass

# root_dir needs a trailing slash (i.e. /root/dir/)
colors_dictionnary = {}
with open('_colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

goodreads = {}
with open('year_first_published_from_goodreads.json', 'r') as fp:
    goodreads = json.load(fp)

i = 0
my_dictionary = {}
for filename in glob.iglob('**/*.yaml', recursive=True):
    # print("-------------")
    basename = os.path.basename(filename)
    if basename[0:1] == "!":
        continue
    if basename == 'app.yaml':
        continue
    print(i, basename)
    parts = PurePath(filename).parts
    house = parts[0]
    folder = parts[len(parts) - 2]
    where = '/' + concatExcludeLast(parts)

    # if not 'enfer' in filename:

    with open(filename, 'r') as f:
        if os.fstat(f.fileno()).st_size != 0: # https://stackoverflow.com/a/283719/1070215
            data = yaml.safe_load(f)
            for key, value in data.items():
                print(key, value)
                value["where"] = where
                tags = value.get("tags", [])
                cover = value.get("cover", {})
                tags.append(folder)
                tags.append(house)
                tags.append(value["lan"])

                found_color = False
                if (key in colors_dictionnary) :
                    if colors_dictionnary[key] is not None:
                        cover = colors_dictionnary[key]
                        found_color = True
                
                if not found_color:
                    print(f"\t{key} <<<<<<<<<<<<<<<<<<< color not found !!!!!!!!!!!!!! run 'python 2create_cover_image_properties.py' ")

                if key in goodreads:
                    if goodreads[key] is not None:
                        # print("found date", key, goodreads[key])
                        tags.append(f"_{goodreads[key]}")

                value["tags"] = tags
                value["cover"] = cover
            my_dictionary.update(data)
    
    i = i + 1

images = []
extensions = ['jpg', 'jpeg', 'webp', 'png']

i = 0
for ext in extensions:
    for filename2 in glob.iglob('thumbs/*.'+ext, recursive=True):
        if ext == 'png':
            print(os.path.basename(i, filename2))
        key = PurePath(filename2).stem[2:]
        images.append(filename2)
        my_dictionary[key]["image_path"] = f"thumbs/{os.path.basename(filename2)}" # filename2

        i = i + 1

print("^^^^^^^^^^^^^^^^^^^^")
j = 0
for key, value in my_dictionary.items():
    if not "image_path" in value:
        print(j, value)
        j = j + 1
print("vvvvvvvvvvvvvvvvvvvv")

with io.open('dist/everything.yaml', 'w',encoding='utf8') as file:
    yaml.dump(my_dictionary, file)

with io.open('images.json', 'w',encoding='utf8') as file2:
    json.dump(images, file2, indent=2)

print(len(my_dictionary))
