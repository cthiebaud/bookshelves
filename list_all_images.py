import glob
import os

i = 0
extensions = ['jpg', 'jpeg', 'webp', 'png']
  
# Using for loop
for ext in extensions:
    for filename in glob.iglob('**/*.'+ext, recursive=True):
        print(os.path.basename(filename))
        i = i + 1


print(i)