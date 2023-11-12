import glob
from PIL import Image

## # get all the jpg files from the current folder
## for infile in glob.glob("*.jpg"):
##   print(infile)
##   im = Image.open(infile)
##   # convert to thumbnail image
##   im.thumbnail((200, 400), Image.LANCZOS)
##   # don't save if thumbnail already exists
##   if infile[0:2] != "T_":
##     # prefix thumbnail file with T_
##     im.save("T_" + infile, "JPEG")

import os
sizes = []
i = 0
for filename3 in glob.iglob('thumbs/*', recursive=False):
  im = Image.open(filename3)
  basename = os.path.basename(filename3)

  size = os.stat(filename3).st_size 
  print(basename, im.size, size)
  sizes.append(size)
  i += 1


print(f"{i} thumbs, {sum(sizes)} total bytes, {min(sizes)} min, {max(sizes)} max")

