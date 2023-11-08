import json
import re

from pathlib import PurePath 
from colorthief import ColorThief

colors_dictionnary = {}

with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

# // sRGB luminance(Y) values
rY = 0.212655
gY = 0.715
bY = 0.072
# // Inverse of sRGB "gamma" function. (approx 2.2)
def inv_gam_sRGB(ic):
    c = ic/255.0
    if c <= 0.04045:
        return c/12.92
    else:
        return pow(((c+0.055)/(1.055)),2.4)

# // sRGB "gamma" function (approx 2.2)
def gam_sRGB(v):
    if v<=0.0031308:
      v *= 12.92
    else: 
      v = 1.055*pow(v,1.0/2.4)-0.055

    return int(v*255+0.5); # // This is correct in C++. Other languages may not require +0.5

# // GRAY VALUE ("brightness")
def gray( r,  g,  b):
    return gam_sRGB(
            rY*inv_gam_sRGB(r) +
            gY*inv_gam_sRGB(g) +
            bY*inv_gam_sRGB(b))

for qwe in colors_dictionnary:
    ## l = colors_dictionnary[qwe]["hls"].split(', ')[1]
    ## print(gam_sRGB(float(l)))

    d = colors_dictionnary[qwe]["dominant_color"]
    print(d)
    matches = re.finditer(r'[\d\.]+', d)
    tup = []
    for matchNum, match in enumerate(matches, start=1):
        tup.append(float(d[match.regs[0][0]:match.regs[0][1]]))   
    g = gray(tup[0], tup[1], tup[2])
    colors_dictionnary[qwe]["luminance"] = g
    del colors_dictionnary[qwe]["gray"]

with open('colors.json', 'w') as fp:
  json.dump(colors_dictionnary, fp, indent=2)

    
