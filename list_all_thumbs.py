import glob
import os

i = 0
directories = ['thumbs', 'thumbs2']
extensions = ['jpg', 'jpeg', 'webp', 'png']
  
# Using for loop
for dir in directories:
    for ext in extensions:
        for filename in glob.iglob(f"{dir}/*.{ext}", recursive=False):
            print(os.path.basename(filename))
            i = i + 1

print(i)