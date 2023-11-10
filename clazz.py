import cv2
import glob
import json
import numpy as np

from pathlib import PurePath 

def classify_color(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert the image from BGR to HSV
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Resize the image if needed
    # image_hsv = cv2.resize(image_hsv, (width, height))
    
    # Calculate the mean value and standard deviation for the saturation channel
    mean_saturation = np.mean(image_hsv[:,:,1])
    std_saturation = np.std(image_hsv[:,:,1])
    mean_hue = np.mean(image_hsv[:,:,0])
    std_hue = np.std(image_hsv[:,:,0])

    # Classify the image based on color
    if mean_saturation < 30 and std_saturation < 10:
        return "White"
    elif mean_saturation < 30 and std_saturation < 50:
        return "Gray"
    elif mean_saturation < 30 and std_saturation >= 50:
        return "Black"
    elif std_hue > 60:
        return "Rainbow"    
    else:
        # Extract dominant hue value
        
        ## print(image_path)

        # Classify based on hue
        if 0 <= mean_hue < 15 or 165 <= mean_hue <= 180:
            return "Red"
        elif 15 <= mean_hue < 45:
            return "Yellow"
        elif 45 <= mean_hue < 75:
            return "Green"
        elif 75 <= mean_hue < 105:
            return "Cyan"
        elif 105 <= mean_hue < 135:
            return "Blue"
        elif 135 <= mean_hue < 165:
            return "Magenta"

## # Example usage
## image_path = "path/to/your/image.jpg"
## classification = classify_color(image_path)
## print(f"The image is classified as: {classification}")


colors_dictionnary = {}
with open('colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

i = 0
# Using for loop
extensions = ['jpg', 'jpeg', 'webp', 'png']
for ext in extensions:
    for filename2 in glob.iglob('thumbs2/*.'+ext, recursive=True):
        key = PurePath(filename2).stem[2:]

        clazz = classify_color(filename2)
        print(key, clazz)
        colors_dictionnary[key]["clazz"] = clazz.lower()

with open('colors.json', 'w') as fp:
    json.dump(colors_dictionnary, fp, indent=2)

