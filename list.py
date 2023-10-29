import glob
import os
from PIL import Image
from operator import attrgetter

# images = []
sizes = []
extensions = ['jpg', 'jpeg', 'webp', 'png']
  
i = 0
# Using for loop
for ext in extensions:
    for filename2 in glob.iglob('**/*.'+ext, recursive=True):

      # if not 'enfer' in filename2:
      
        # images.append(filename2)
        # print(os.path.basename(filename2))

        im = Image.open(filename2)
        size = os.stat(filename2).st_size
        sizes.append(size)
        if size > 1000000 :
            print(os.stat(filename2).st_size, im.size, im.format, filename2)
        i += 1


print(i, sum(sizes), min(sizes), max(sizes))
