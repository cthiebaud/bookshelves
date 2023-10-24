import glob
import os
import io

# import pyyaml module
import yaml
import json
    
from pathlib import PurePath 

def concatExcludeLast(strlst):
    return '/'.join(strlst[0:-1])


try:
    os.remove('everything.yaml')
except OSError:
    pass

# root_dir needs a trailing slash (i.e. /root/dir/)
i = 0
my_dictionary = {}
images = []
for filename in glob.iglob('**/*.yaml', recursive=True):
    # print("-------------")
    print(i, os.path.basename(filename))
    parts = PurePath(filename).parts
    where = '/' + concatExcludeLast(parts)

    locationTag = parts[len(parts) - 2]

    # if not 'enfer' in filename:

    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        for key, value in data.items():
            data[key]["where"] = where
            tags = value.get("tags", [])
            tags.append(locationTag)
            value["tags"] = tags
        my_dictionary.update(data)


extensions = ['jpg', 'jpeg', 'webp', 'png']
  
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('**/*.'+ext, recursive=True):

      # if not 'enfer' in filename2:
      
        # print(i, filename2)
        # print(os.path.basename(filename2))
        images.append(filename2)
        my_dictionary[PurePath(filename2).stem]["image_path"] = filename2



print("^^^^^^^^^^^^^^^^^^^^")
j = 0
for key, value in my_dictionary.items():
    if not "image_path" in value:
        print(j, value)
        j = j + 1
print("vvvvvvvvvvvvvvvvvvvv")

with io.open('everything.yaml', 'w',encoding='utf8') as file:
    yaml.dump(my_dictionary, file)

with io.open('images.json', 'w',encoding='utf8') as file2:
    json.dump(images, file2, indent=2)


print(len(my_dictionary))
