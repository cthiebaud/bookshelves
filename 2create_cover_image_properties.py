import cv2
import glob
import json
import numpy as np
import sys

from collections import Counter
from pathlib import PurePath 
from sklearn.cluster import KMeans

## https://stackoverflow.com/a/57986495/1070215
import warnings
warnings.filterwarnings("ignore")

monos = []

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

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RANSACRegressor
from sklearn.metrics import mean_squared_error

def rgb_to_lab(rgb):
    # Convert RGB to Lab
    lab = cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2LAB)[0][0]
    return lab

def lab_to_rgb(lab):
    # Convert Lab to RGB
    rgb = cv2.cvtColor(np.uint8([[lab]]), cv2.COLOR_LAB2RGB)[0][0]
    return rgb

def compute_monochromatic_score(original_image):
    # Load the image
    ## original_image = cv2.imread(image_path)

    # Get the shape of the image
    height, width, _ = original_image.shape

    original_image_normalized = original_image / 255.0

    # Reshape the image to a 1D array
    rgb_triplets = original_image_normalized.reshape((height * width, 3))

    # Convert RGB to Lab
    lab_triplets = np.array([rgb_to_lab(rgb) for rgb in rgb_triplets])

    # Apply weights to Lab channels
    lab_triplets[:, 0] = (lab_triplets[:, 0] * 0.1).astype(np.uint8)  # Lightness channel weight

    # Fit a straight line using RANSAC
    model = RANSACRegressor().fit(lab_triplets, lab_triplets)

    # Fit a straight line to the Lab triplets
    # model = LinearRegression().fit(lab_triplets, lab_triplets)

    # Predict the Lab values on the line
    predicted_lab = model.predict(lab_triplets)

    # Convert predicted Lab values back to RGB
    predicted_rgb = np.array([lab_to_rgb(lab) for lab in predicted_lab])

    # Calculate the least squares error
    mse = mean_squared_error(rgb_triplets, predicted_rgb)

    # Define a threshold for monochromatic score
    threshold = 0.0001  # You may need to adjust this based on your specific use case

    monos.append(mse)

    # Determine the monochromatic score
    monochromatic_score = "Monochromatic" if mse < threshold else "Colorful"

    return monochromatic_score, mse


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

    return dominant_colors_info


def calc_image_properties(image_path):

    properties = {}
    
    # Read the image
    image = cv2.imread(image_path)

    if True:
        monochromatic_score, mean_squared_error = compute_monochromatic_score( image.copy())
        properties["monochromatic_mean_squared_error"] = f"{mean_squared_error}"

    if True:
        dom = calculate_dominant_colors(image.copy(), 5) ## 
        ####, pal 
        properties["palette"] = f"{dom}"
        #### properties["palette_diversity"] = f"{pal}"

    if False:
        mono = calculate_monochrome( image.copy())
        properties["monochrome"] = f"{mono}"
    
    if False:
        mono2 = calculate_monochrome2( image.copy())
        properties["monochrome2"] = f"{mono2}"

    return properties

colors_dictionnary = {}
with open('_colors.json', 'r') as fp:
    colors_dictionnary = json.load(fp)

i = 0
# Using for loop
extensions = ['jpg', 'jpeg', 'webp', 'png']

arguments = []
first_argument = None
if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    first_argument = arguments[0]

for ext in extensions:
    for filename2 in glob.iglob('thumbs2/*.'+ext, recursive=True):
        key = PurePath(filename2).stem[2:]
        ## print(f"(key not in colors_dictionnary): {key not in colors_dictionnary} or (key in arguments): {key in arguments} or (first_argument == '*'): {first_argument}")
        if (key not in colors_dictionnary) or (key in arguments) or (first_argument == '*'):
            print(i, key, "...")
            properties = calc_image_properties(filename2)
            print(i, key, properties)
            colors_dictionnary[key] = properties 
            ## {
            ##     "properties": properties
            ## }
        i = i + 1

with open('_colors.json', 'w') as fp:
    json.dump(colors_dictionnary, fp, indent=2)

print(f"mse: min {min(monos)} max {max(monos)}")

