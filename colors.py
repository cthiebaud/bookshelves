import colorsys
import glob
import json
import os
import sys
import webcolors
import yaml
import cv2
import numpy as np


import sys
import numpy as np
from skimage import io
from skimage.transform import resize
from skimage.exposure import is_low_contrast

from pathlib import PurePath 
from colorthief import ColorThief

colors_dictionnary = {}

## https://stackoverflow.com/a/58826063/1070215
def getContrast(file):

    # load image as YUV (or YCbCR) and select Y (intensity)
    # or convert to grayscale, which should be the same.
    # Alternately, use L (luminance) from LAB.
    img = cv2.imread(file)
    Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:,:,0]

    # compute min and max of Y
    min = np.min(Y)
    max = np.max(Y)

    contrast = 0
    # compute contrast
    if max+min != 0:
        contrast = (max-min)/(max+min)
    # print(min,max,contrast)    
    return contrast

def getMonochrome(im):

    # Down-res image to make SVD time reasonable
    im = resize(im,(128,128))

    # Form list of all RGB triplets present in image
    triplets = im.reshape(-1,3)

    # Get mean on all axes
    means = triplets.mean(axis=0)

    # Calculate SVD
    uu, dd, vv = np.linalg.svd(triplets - means)

    # dd holds the variance in each of the PCA directions
    # The key factor is what percentage of the variance is held in the first direction
    PC1var = dd[0]*100./dd.sum()
    PC2var = dd[1]*100./dd.sum()
    PC3var = dd[2]*100./dd.sum()
    ## print(f"PC1 variance: {PC1var}")
    ## print(f"PC2 variance: {PC2var}")
    ## print(f"PC3 variance: {PC3var}")

    return PC1var


with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

i = 0
# Using for loop
extensions = ['jpg', 'jpeg', 'webp', 'png']
for ext in extensions:
    for filename2 in glob.iglob('thumbs2/*.'+ext, recursive=True):

        # print(os.path.basename(filename2))
        key = PurePath(filename2).stem[2:]

        print(i, key)
        i = i + 1
##             if is_low_contrast(im, fraction_threshold=0.5): 
##                 print("  low contrast")
##                 if (monochrome(im)) :
##                     print("    monochrome")

        color_thief = ColorThief(filename2)
        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)
        r,g,b = dominant_color
        dominant_color_string = f"rgb({r}, {g}, {b})"
        h,l,s = colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0)

        if key in colors_dictionnary:
            colors_dictionnary[key]["hls"] = f"{h}, {l}, {s}"
        else:
            contrast = getContrast(filename2)
            im = io.imread(filename2)
            monochrome = getMonochrome(im)

            colors_dictionnary[key] = {"dominant_color": dominant_color_string, "contrast": contrast, "monochrome": monochrome}
            print("    ", colors_dictionnary[key])

##             ##            
##             ##            colors_dictionnary[key]["dominant_color"] = dominant_color_string
##             ##            colors_dictionnary[key]["clazz"] = clazz
##             ##
##                     print("      " + clazz)
            
##
#  
with open('colors.json', 'w') as fp:
  json.dump(colors_dictionnary, fp, indent=2)


