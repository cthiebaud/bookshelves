import glob
from pathlib import PurePath 

extensions = ['jpg', 'jpeg', 'webp', 'png']

with open('isbn-nein.txt', 'w') as fNein:
    with open('isbn-ja.txt', 'w') as fJa:

        for ext in extensions:
            covers = f"/Users/christophe.thiebaud/github.com/cthiebaud/bookshelves/thumbs/*.{ext}"
            i = 0
            for filename in glob.iglob(covers):
                isbn = PurePath(filename).stem[2:]
                if not isbn.startswith("978") and not isbn.startswith("979") and not isbn.startswith("977"):
                    # print(isbn)
                    fNein.write(f"https://www.goodreads.com/book/isbn/{isbn}\n")
                else:
                    fJa.write(f"{isbn}\n")


 