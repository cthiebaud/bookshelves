import glob
import os
from PIL import Image
from operator import attrgetter

sizes = []
extensions = ['jpg', 'jpeg', 'webp', 'png']
i = 0
for ext in extensions:
    for filename in glob.iglob('/Users/christophe.thiebaud/github.com/cthiebaud/bookcovers/covers/*.'+ext, recursive=True):
        
        # count
        size = os.stat(filename).st_size
        sizes.append(size)
        i += 1

        basename = os.path.basename(filename)
        newName = "/Users/christophe.thiebaud/github.com/cthiebaud/bookshelves/thumbs/T_" + basename
        # don't create thumbnail if already exists
        if not os.path.isfile(newName):
          print(f"{basename} => {newName}")
          im = Image.open(filename).convert('RGB')

          im.thumbnail((200, 400), Image.LANCZOS)
          # prefix thumbnail file with T_
          im.save(newName, "JPEG")
        
 
## for filename3 in glob.iglob('thumbs/*', recursive=False):
##   size = os.stat(filename3).st_size 
##   sizes.append(size)
##   i += 1
## 
## 
## print(i, sum(sizes), min(sizes), max(sizes))
