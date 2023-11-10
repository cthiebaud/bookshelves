import cv2
import glob
import json
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from collections import Counter
from pathlib import PurePath 
from sklearn.cluster import KMeans

def calculate_dominant_colors(image, k=3):
    # Read the image
    # image = cv2.imread(image_path)

    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a 2D array of pixels
    pixels = image_rgb.reshape(-1, 3)

    # Use K-Means clustering to find the dominant colors
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers (dominant colors)
    dominant_colors = kmeans.cluster_centers_

    # Convert RGB values to integers
    dominant_colors = dominant_colors.round().astype(int)

    # Use Counter to count the occurrences of each dominant color
    color_labels = kmeans.labels_
    color_counts = Counter(color_labels)

    # Organize the dominant colors and their counts
    dominant_colors_info = []
    for color, count in color_counts.items():
        rgb_color = dominant_colors[color].tolist()
        dominant_colors_info.append({
            "color": rgb_color,
            "count": count
        })

    return dominant_colors_info

def classify_color(image_path, properties):
    # Read the image
    image = cv2.imread(image_path)

    dom = calculate_dominant_colors(image)

    properties["most_common"] = f"{dom}"
    
    # Convert the image from BGR to HSV
    # image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)    
    # Resize the image if needed
    # image_hsv = cv2.resize(image_hsv, (width, height))
    
    # Calculate the mean value and standard deviation for the saturation channel
    mean_hue = properties["mean_hue"] = np.mean(image_hsl[:, :, 0])
    std_hue = properties["std_hue"] = np.std(image_hsl[:, :, 0])
    mean_lightness = properties["mean_lightness"] = np.mean(image_hsl[:, :, 1])
    std_lightness = properties["std_lightness"] = np.std(image_hsl[:, :, 1])
    mean_saturation = properties["mean_saturation"] = np.mean(image_hsl[:, :, 2])
    std_saturation = properties["std_saturation"] = np.std(image_hsl[:, :, 2])

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
        if key not in colors_dictionnary:
            properties = {}
            clazz = classify_color(filename2, properties)
            print(i, key, clazz, properties)
            colors_dictionnary[key] = {
                "clazz": clazz.lower(),
                "properties": properties
            }
        i = i + 1

with open('colors.json', 'w') as fp:
    json.dump(colors_dictionnary, fp, indent=2)

