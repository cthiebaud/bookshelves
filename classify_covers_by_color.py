import cv2
import glob
import json
import numpy as np

from collections import Counter
from pathlib import PurePath 
from sklearn.cluster import KMeans

## https://stackoverflow.com/a/57986495/1070215
import warnings
warnings.filterwarnings("ignore")

####    import warnings
####    warnings.filterwarnings("ignore")
####
####    from colormath.color_diff import delta_e_cie2000
####    from colormath.color_objects import LabColor, sRGBColor
####    from colormath.color_conversions import convert_color
####    
####    # Function to calculate CIEDE2000 color difference between two LAB color values
####    def ciede2000_color_difference(Lab1, Lab2):
####        L1, a1, b1 = Lab1
####        L2, a2, b2 = Lab2
####    
####        # Constants for CIEDE2000 calculation
####        KL = 1
####        KC = 1
####        KH = 1
####    
####        def delta_L(L1, L2):
####            return L2 - L1
####    
####        def delta_C(C1, C2):
####            return C2 - C1
####    
####        def delta_H(H1, H2, C1, C2):
####            delta_h = H2 - H1
####            delta_h = np.where(np.abs(delta_h) <= 180, delta_h, np.where(delta_h > 0, delta_h - 360, delta_h + 360))
####            return 2 * np.sqrt(C1 * C2) * np.sin(np.radians(delta_h / 2))
####    
####        def mean(a, b):
####            return (a + b) / 2
####    
####        def mean_L(L1, L2):
####            return mean(L1, L2)
####    
####        def mean_C(C1, C2):
####            return mean(C1, C2)
####    
####        def mean_H(H1, H2, C1, C2):
####            return mean(H1, H2) + np.where(np.abs(H1 - H2) > 180, 180, 0)
####    
####        def C_prime(C, L):
####            return np.sqrt(C**2 + KL * (L - 50)**2)
####    
####        def H_prime(H, C, L):
####            return np.rad2deg(np.arctan2(C * np.sin(np.radians(H)), C * np.cos(np.radians(H))))
####    
####    
####        C1 = np.sqrt(a1**2 + b1**2)
####        C2 = np.sqrt(a2**2 + b2**2)
####    
####        L1, L2 = mean_L(L1, L2)
####        C1, C2 = mean_C(C1, C2)
####        H1, H2 = mean_H(H_prime(a1, C1, L1), H_prime(a2, C2, L2), C1, C2)
####    
####        delta_L_ = delta_L(L1, L2)
####        delta_C_ = delta_C(C1, C2)
####        delta_H_ = delta_H(H1, H2, C1, C2)
####    
####        SL = 1 + (0.015 * (L1 - 50)**2) / np.sqrt(20 + (L1 - 50)**2)
####        SC = 1 + 0.045 * C1
####        SH = 1 + 0.015 * C1 * (1 - np.cos(np.radians(H1 - 160)))
####    
####        delta_theta = 30 * np.exp(-((H_prime(a1, C1, L1) - 275) / 25)**2)
####        RC = 2 * np.sqrt(C1**7 / (C1**7 + 25**7))
####        RT = -RC * np.sin(np.radians(2 * delta_theta))
####    
####        return np.sqrt((delta_L_ / (KL * SL))**2 + (delta_C_ / (KC * SC))**2 + (delta_H_ / (KH * SH))**2 + RT * (delta_C_ / (KC * SC)) * (delta_H_ / (KH * SH)))
####    
####    ## # Your color palette as a list of BGR values
####    ## palette = [
####    ##     (0, 0, 255),  # Red
####    ##     (0, 255, 0),  # Green
####    ##     (255, 0, 0),  # Blue
####    ##     # Add more colors
####    
####    def calculate_palette_diversity(palette):
####        # Convert BGR colors to LAB colors
####        lab_palette = [cv2.cvtColor(
####                np.uint8([[color]]), 
####                cv2.COLOR_BGR2Lab
####            )[0, 0] 
####            for color in palette]
####    
####        # Calculate the color differences between all pairs of colors
####        total_difference = 0
####        pair_count = 0
####    
####        for i in range(len(lab_palette)):
####            for j in range(i + 1, len(lab_palette)):
####                diff = ciede2000_color_difference(lab_palette[i], lab_palette[j])
####                total_difference += diff
####                pair_count += 1
####    
####        # Calculate the average color difference as the diversity indicator
####        diversity_indicator = total_difference / pair_count
####    
####        print('Diversity Indicator:', diversity_indicator)
####    
####        return diversity_indicator
####    
####    
# https://stackoverflow.com/a/59218331/1070215
def calculate_monochrome(im):

    # Down-res image to make SVD time reasonable
    im = cv2.resize(im, (128, 128))

    # Convert the image to the format expected by SVD
    triplets = im.reshape(-1, 3)

    # Get mean on all axes
    means = triplets.mean(axis=0)

    # Calculate SVD
    triplets_centered = triplets - means
    uu, dd, vv = np.linalg.svd(triplets_centered)

    # dd holds the variance in each of the PCA directions
    # The key factor is what percentage of the variance is held in the first direction
    PC1var = dd[0] * 100.0 / dd.sum()
    PC2var = dd[1] * 100.0 / dd.sum()
    PC3var = dd[2] * 100.0 / dd.sum()
    print(f"MONOCHROME, PC1 variance: {PC1var}; PC2 variance: {PC2var}; PC3 variance: {PC3var}")

    return PC1var

def calculate_monochrome2(image):

    # Convert the image to the LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Calculate the color histogram
    hist = cv2.calcHist([lab_image], [1, 2], None, [256, 256], [0, 256, 0, 256])

    # Calculate the total number of pixels in the image
    total_pixels = lab_image.shape[0] * lab_image.shape[1]

    # Calculate the percentage of the most dominant color in the image
    dominant_color_percentage = (hist.max() / total_pixels) * 100

    return dominant_color_percentage


def calculate_dominant_colors(image, k=5):
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
    palette= []
    for color, count in color_counts.items():
        rgb_color = dominant_colors[color].tolist()
        palette.append(dominant_colors[color])
        dominant_colors_info.append({
            "color": rgb_color,
            "count": count
        })

    #### palette_diversity = calculate_palette_diversity(palette)

    return dominant_colors_info ####, palette_diversity

def classify_color(image_path, properties):
    # Read the image
    image = cv2.imread(image_path)

    if True:
        dom = calculate_dominant_colors(image, 5) ## .copy()
        ####, pal 
        properties["most_common"] = f"{dom}"
        #### properties["palette_diversity"] = f"{pal}"

    if False:
        mono = calculate_monochrome( image.copy())
        properties["monochrome"] = f"{mono}"
    
    if False:
        mono2 = calculate_monochrome2( image.copy())
        properties["monochrome2"] = f"{mono2}"

    # Convert the image from BGR to HSV
    # image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    ## 
    # image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)    
    # Resize the image if needed
    # image_hsv = cv2.resize(image_hsv, (width, height))
    
    ## # Calculate the mean value and standard deviation for the saturation channel
    ## mean_hue = properties["mean_hue"] = np.mean(image_hsl[:, :, 0])
    ## std_hue = properties["std_hue"] = np.std(image_hsl[:, :, 0])
    ## mean_lightness = properties["mean_lightness"] = np.mean(image_hsl[:, :, 1])
    ## std_lightness = properties["std_lightness"] = np.std(image_hsl[:, :, 1])
    ## mean_saturation = properties["mean_saturation"] = np.mean(image_hsl[:, :, 2])
    ## std_saturation = properties["std_saturation"] = np.std(image_hsl[:, :, 2])

    ## # Classify the image based on color
    ## if mean_saturation < 30 and std_saturation < 10:
    ##     return "White"
    ## elif mean_saturation < 30 and std_saturation < 50:
    ##     return "Gray"
    ## elif mean_saturation < 30 and std_saturation >= 50:
    ##     return "Black"
    ## elif std_hue > 60:
    ##     return "Rainbow"    
    ## else:
    ##     # Extract dominant hue value
    ##     
    ##     ## print(image_path)
    ##   
    ##     # Classify based on hue
    ##     if 0 <= mean_hue < 15 or 165 <= mean_hue <= 180:
    ##         return "Red"
    ##     elif 15 <= mean_hue < 45:
    ##         return "Yellow"
    ##     elif 45 <= mean_hue < 75:
    ##         return "Green"
    ##     elif 75 <= mean_hue < 105:
    ##         return "Cyan"
    ##     elif 105 <= mean_hue < 135:
    ##         return "Blue"
    ##     elif 135 <= mean_hue < 165:
    ##         return "Magenta"

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
            print(i, key, "...")
            properties = {}
            clazz = classify_color(filename2, properties)
            print(i, key, clazz, properties)
            colors_dictionnary[key] = {
                "properties": properties
            }
        i = i + 1

with open('colors.json', 'w') as fp:
    json.dump(colors_dictionnary, fp, indent=2)

