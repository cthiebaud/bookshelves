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
    ## Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:,:,0]
## 
    ## # compute min and max of Y
    ## min = np.min(Y)
    ## max = np.max(Y)
## 
    ## contrast = None
    ## # compute contrast
    ## if max == 0 and min == 0:
    ##     contrast = 0
    ## else:
    ##     contrast = (max-min)/(max+min)
    ## print("CONTRAST", min, max, contrast)    

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast = img_grey.std()
    print("CONTRAST", contrast)    
    return contrast

# https://stackoverflow.com/a/59218331/1070215
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
    print(f"MONOCHROME, PC1 variance: {PC1var}; PC2 variance: {PC2var}; PC3 variance: {PC3var}")

    return PC1var

# https://stackoverflow.com/a/3244061/1070215
def getDominant(file):
    ## print('reading image')
    from PIL import Image
    import scipy
    import scipy.misc
    import scipy.cluster
    import binascii

    NUM_CLUSTERS = 5

    im = Image.open(file)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    ## print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    ## print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('DOMINANT COLOR %s (#%s)' % (peak, colour))
    return peak


with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

i = 0
# Using for loop
extensions = ['jpg', 'jpeg', 'webp', 'png']
for ext in extensions:
    for filename2 in glob.iglob('thumbs2/*.'+ext, recursive=True):

        # print(os.path.basename(filename2))
        key = PurePath(filename2).stem[2:]

        ## if key != "978-2823609851":
        ##     continue

        print(i, key)
##             if is_low_contrast(im, fraction_threshold=0.5): 
##                 print("  low contrast")
##                 if (monochrome(im)) :
##                     print("    monochrome")

        # color_thief = ColorThief(filename2)
        # dominant_color = color_thief.get_color(quality=1)
        # get the dominant color

        if key not in colors_dictionnary:
            # print(i, "skip")
            # colors_dictionnary[key]["hls"] = f"{h}, {l}, {s}"       
            # colors_dictionnary[key]["dominant_color"] = dominant_color_string      
        # else:

            contrast = getContrast(filename2)
            im = io.imread(filename2)
            monochrome = getMonochrome(im)

            dominant_color = getDominant(filename2)
            r,g,b = dominant_color
            ## print(dominant_color)
            dominant_color_string = f"rgb({r}, {g}, {b})"
            h,l,s = colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0)
            colors_dictionnary[key] = {
                "dominant_color": dominant_color_string, 
                "hls": f"{h}, {l}, {s}", 
                "monochrome_variance": monochrome,
                "contrast": contrast} 
            print("========>", colors_dictionnary[key])
            with open('colors.json', 'w') as fp:
              json.dump(colors_dictionnary, fp, indent=2)

        i = i + 1

##             ##            
##             ##            colors_dictionnary[key]["dominant_color"] = dominant_color_string
##             ##            colors_dictionnary[key]["clazz"] = clazz
##             ##
##                     print("      " + clazz)
            
##
#  
with open('colors.json', 'w') as fp:
  json.dump(colors_dictionnary, fp, indent=2)


