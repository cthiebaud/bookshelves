import glob
from PIL import Image

# get all the jpg files from the current folder
for infile in glob.glob("*.jpg"):
  print(infile)
  im = Image.open(infile)
  # convert to thumbnail image
  im.thumbnail((200, 400), Image.LANCZOS)
  # don't save if thumbnail already exists
  if infile[0:2] != "T_":
    # prefix thumbnail file with T_
    im.save("T_" + infile, "JPEG")
