import glob
import os
from PIL import Image
from operator import attrgetter

# images = []
sizes = []
extensions = ['jpg', 'jpeg', 'webp', 'png']
  
i = 0

## # Using for loop
## for ext in extensions:
##     for filename2 in glob.iglob('**/[!T]*.'+ext, recursive=True):
## 
##       # if not 'enfer' in filename2:
##       
##         # images.append(filename2)
##         # print(os.path.basename(filename2))
## 
##         im = Image.open(filename2).convert('RGB')
##         size = os.stat(filename2).st_size
##         sizes.append(size)
##         i += 1
##         # if size > 100000 :
##         # print(os.stat(filename2).st_size, im.size, im.format, filename2)
## 
##         im.thumbnail((200, 400), Image.LANCZOS)
##         # don't save if thumbnail already exists
##         basename = os.path.basename(filename2)
##         # if basename[0:2] != "T_":
##         #   print(basename)
##         #   # prefix thumbnail file with T_
##         #   newName = "/Users/christophe.thiebaud/github.com/cthiebaud/bookshelves/thumbs/T_" + basename
##         #   print(newName)
##         #   im.save(newName, "JPEG")
## # 

for filename3 in glob.iglob('thumbs/*', recursive=False):
  size = os.stat(filename3).st_size 
  sizes.append(size)
  i += 1


print(i, sum(sizes), min(sizes), max(sizes))
