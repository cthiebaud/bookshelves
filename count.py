import os
import re
import sys

rootdir = "."
count = 0

for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.yaml'):
            fullpath = os.path.join(root, file)
            with open(fullpath) as f:
                for line in f:
                    if re.search(sys.argv[1], line):
                        print(line)
                        count = count + 1


if count > 0:
    print(count)
else: 
    print("No results.")