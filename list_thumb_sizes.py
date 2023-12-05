import glob
from PIL import Image
from statistics import mean, median, stdev, variance

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
ratios = []
imsizes = []
i = 0
for filename3 in glob.iglob('thumbs/*', recursive=False):
  im = Image.open(filename3)
  basename = os.path.basename(filename3)

  size = os.stat(filename3).st_size 
  print(basename, im.size, size)
  sizes.append(size)
  imsizes.append(im.size)
  ratios.append(im.size[1]/im.size[0])

  i += 1


print(f"{i} thumbs, {sum(sizes)} total bytes, {min(sizes)} min, {max(sizes)} max")
print(f"{min(imsizes, key = lambda t: t[0])} min width, {max(imsizes, key = lambda t: t[0])} max width")
print(f"{min(imsizes, key = lambda t: t[1])} min height, {max(imsizes, key = lambda t: t[1])} max height")
print(f"ratio: {min(ratios)} min, {max(ratios)} max, {mean(ratios)} mean, {median(ratios)} median, {stdev(ratios)} stdev, {variance(ratios)} variance")

