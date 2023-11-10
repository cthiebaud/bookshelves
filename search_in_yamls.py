import os
import re
import sys


if len(sys.argv) < 2:
    print(f"* - - -\n{sys.argv[0]} expects one argument: a regular expression, e.g.\n\n\tpython {sys.argv[0]} '^\d{{3}}-2'\n\n- - - *")
    sys.exit() 

rootdir = "."
count = 0
printNext = False
lastLine = None
lineNumber = 0
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.yaml'):
            fullpath = os.path.join(root, file)
            lineNumber = 0
            with open(fullpath) as f:
                for line in f:
                    if printNext:
                        print(line)
                        printNext = False
                    if re.search(sys.argv[1], line):
                        print(f"{fullpath}, around line {lineNumber}:")
                        if lastLine is not None:
                            print(lastLine.replace("\n", ""))
                        print(line.replace("\n", ""))
                        printNext = True
                        count = count + 1
                    lastLine = line
                    lineNumber = lineNumber + 1



if count > 0:
    print(f"{count} results")
else: 
    print("No results.")