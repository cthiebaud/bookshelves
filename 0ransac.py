import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

# Load the example image
image_path = "thumbs2/T_978-0330262132.jpg"
original_image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

# Get the image shape
height, width, _ = image_rgb.shape

# Reshape the image to a 1D array
rgb_triplets = image_rgb.reshape((height * width, 3))

# Apply RANSACRegressor
ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
ransac.fit(rgb_triplets, rgb_triplets)

# Define the plane equation
def z(x, y):
    return (-ransac.estimator_.intercept_ - ransac.estimator_.coef_[0] * x - ransac.estimator_.coef_[1] * y) / ransac.estimator_.coef_[2]

# Create a scatter plot for RGB triplets
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Convert RGB triplets to uint8 for scatter plot
rgb_triplets_uint8 = (rgb_triplets * 255).astype(np.uint8)

# Plot RGB triplets as a scatter plot
sc = ax.scatter(rgb_triplets[:, 0], rgb_triplets[:, 1], rgb_triplets[:, 2], c=rgb_triplets_uint8 / 255.0, cmap='viridis', s=1)

# Add colorbar
cbar = fig.colorbar(sc)

# Set axis labels
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')

plt.show()
