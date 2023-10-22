import glob
import os
import io

# import pyyaml module
import yaml

from pathlib import PurePath 

def conexclast(strlst):
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
    # print(i, os.path.basename(filename))
    where = '/' + conexclast(PurePath(filename).parts)

    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        for key, value in data.items():
            data[key]["where"] = where
        my_dictionary.update(data)


extensions = ['jpg', 'jpeg', 'webp', 'png']
  
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('**/*.'+ext, recursive=True):
        # print(i, filename)
        # print(os.path.basename(filename2))
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

print(len(my_dictionary))
