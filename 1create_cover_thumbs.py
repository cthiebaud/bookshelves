import glob
import os
from PIL import Image
from pathlib import PurePath 

extensions = ['jpg', 'jpeg', 'webp', 'png']
directories = [("covers-no-text","thumbs2"), ("covers","thumbs")]

i = 0
created = 0
for ext in extensions:
  for dir in directories:
    covers = f"/Users/christophe.thiebaud/github.com/cthiebaud/bookcovers/{dir[0]}/*.{ext}"
    thumbs = dir[1]
    for filename in glob.iglob(covers):
        key = ''
        stem = PurePath(filename).stem

        if stem[0] == 'Z':
           key = stem[2:]
        elif stem[0] == 'N':
           key = stem[2:]
        else:
          key = stem
        # prefix thumbnail file with T_
        thumbName = f"{dir[1]}/T_{key}.webp"
        print(i, filename, "=>", thumbName, os.path.isfile(thumbName))
        
        # don't create thumbnail if already exists
        if not os.path.isfile(thumbName):
          print(f"{key} => {thumbName}")
          im = Image.open(filename).convert('RGBA')
          im.thumbnail((200, 400), Image.LANCZOS)
          im.save(thumbName, format='WebP')
          created = created + 1
        
        i = i + 1

      
print(f"2 x {created/2} thumb(s) created out of {i} images crawled, {i-created} already exist")