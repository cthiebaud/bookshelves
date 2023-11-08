import glob
from pathlib import PurePath 
from PIL import Image

extensions = ['jpg', 'jpeg', 'webp', 'png']

with open('non-isbn.txt', 'w') as f:

    for ext in extensions:
        covers = f"/Users/christophe.thiebaud/github.com/cthiebaud/bookshelves/thumbs/*.{ext}"
        i = 0
        for filename in glob.iglob(covers):
            isbn = PurePath(filename).stem[2:]
            if not isbn.startswith("978") and not isbn.startswith("979") :
                print(isbn)
                f.write(f"{isbn}\n")

 