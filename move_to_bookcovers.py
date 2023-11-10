import glob
import os
from PIL import Image
from operator import attrgetter

# images = []
sizes = []
extensions = ['jpg', 'jpeg', 'webp', 'png']
  
i = 0

## # Using for loop
for ext in extensions:
  for filename2 in glob.iglob('**/[!T]*.'+ext, recursive=True):
    os.rename(filename2, "/Users/christophe.thiebaud/github.com/cthiebaud/bookcovers/covers/"+os.path.basename(filename2))

