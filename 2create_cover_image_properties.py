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

    image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Get the shape of the image
    height, width, _ = image_rgb.shape

    original_image_normalized = image_rgb / 255.0

    # Reshape the image to a 1D array
    rgb_triplets = original_image_normalized.reshape((height * width, 3))

    # Fit a plane using RANSAC
    model = RANSACRegressor().fit(rgb_triplets, rgb_triplets)

    # Get the coefficients of the plane
    plane_coefficients = model.estimator_.coef_

    # Extract coefficients for the plane equation ax + by + cz + d = 0
    a, b, c = plane_coefficients[:, -1]
    d = model.estimator_.intercept_
    # Convert to a JavaScript-friendly format
    plane_coefficients_js = [float(a), float(b), float(c), float(d)]

    # Perform linear regression on 2D coordinates within the plane
    plane_points_2d = rgb_triplets[:, :2]
    linear_model_on_plane = LinearRegression().fit(plane_points_2d, rgb_triplets)

    # Get the coefficients of the line within the plane
    line_coefficients = linear_model_on_plane.coef_

    # Extract coefficients for the line equation mx + ny + p = 0
    m, n, p = line_coefficients[:, -1]

    # Convert to a JavaScript-friendly format
    line_coefficients_js = [float(m), float(n), float(p)]    

    # Predict the RGB values on the plane
    predicted_rgb_on_plane = model.predict(rgb_triplets)
    # Calculate the least squares error for the plane
    mse_plane = mean_squared_error(rgb_triplets, predicted_rgb_on_plane)

    # Predict the RGB values on the line within the plane
    predicted_rgb_on_line = linear_model_on_plane.predict(plane_points_2d)
    # Calculate the least squares error for the line within the plane
    mse_line_within_plane = mean_squared_error(rgb_triplets, predicted_rgb_on_line)

    return mse_plane, plane_coefficients_js, mse_line_within_plane, line_coefficients_js

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

    if False:
        mse_plane, plane_coefficients, mse_line_within_plane, line_coefficients = compute_monochromatic_score( image.copy())
        properties["mse_plane"] = f"{mse_plane}"
        properties["plane_coefficients"] = f"{plane_coefficients}"
        properties["mse_line_within_plane"] = f"{mse_line_within_plane}"
        properties["line_coefficients"] = f"{line_coefficients}"

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
