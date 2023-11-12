import glob
import os
from PIL import Image

extensions = ['jpg', 'jpeg', 'webp', 'png']
directories = [("covers-no-text","thumbs2"), ("covers","thumbs")]

i = 0
created = 0
for ext in extensions:
  ## print(ext) 
  for dir in directories:
    ## print(dir[0], "=>", dir[1]) 
    covers = f"/Users/christophe.thiebaud/github.com/cthiebaud/bookcovers/{dir[0]}/*.{ext}"
    thumbs = dir[1]
    for filename in glob.iglob(covers):
        basename = os.path.basename(filename)
        if basename[0] == 'Z':
           basename = basename[2:]
        # if basename.startswith('978-2070514427') :
          # prefix thumbnail file with T_
        thumbName = f"{dir[1]}/T_{basename}"
        # print(i, filename, "=>", thumbName, os.path.isfile(thumbName))
        
        # don't create thumbnail if already exists
        if not os.path.isfile(thumbName):
          print(f"{basename} => {thumbName}")
          im = Image.open(filename).convert('RGB')
          im.thumbnail((200, 400), Image.LANCZOS)
          im.save(thumbName, "JPEG")
          created = created + 1
        
        i = i + 1

      
print(f"{created} thumb(s) created out of {i} images crawled, {i-created} already exist")