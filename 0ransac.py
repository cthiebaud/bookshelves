import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

# Load the example image
image_path = "thumbs2/T_979-1092457186.jpg"
original_image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

# Get the image shape
height, width, _ = image_rgb.shape

# Reshape the image to a 1D array
rgb_triplets = image_rgb.reshape((height * width, 3))

# Split rgb_triplets into rg_tuples and b_singleton
rg_tuples = rgb_triplets[:, :2]  # Take the first two elements (r and g)
b_singleton = rgb_triplets[:, 2].reshape((-1, 1))  # Take the third element (b) and reshape to column vector


# Apply RANSACRegressor
ransac = linear_model.RANSACRegressor(linear_model.LinearRegression()) # fit_intercept=True
ransac.fit(rg_tuples, b_singleton)

# Access the coefficients and intercept
matrix = ransac.estimator_.coef_
interc = ransac.estimator_.intercept_

print(matrix, interc)

### # Extract coefficients
### X = matrix[0, :]
### Y = matrix[1, :]
### Z = matrix[2, :]
### 
### # Formulate the system of equations
### A = np.vstack([X, Y, Z, np.ones_like(X)]).T
### 
### # Solve the system of equations
### a, b, c = np.linalg.lstsq(A[:, :-1], -A[:, -1], rcond=None)[0]

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
## cbar = fig.colorbar(sc)

# Set axis labels
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')

### # Define the points on the plane 11x - 13y + 5z - 23 = 0
### x_plane = np.linspace(0, 255, 100)
### y_plane = np.linspace(0, 255, 100)
### x_plane, y_plane = np.meshgrid(x_plane, y_plane)
### z_plane = (a * x_plane + b * y_plane) / c
### 
### # Plot the plane
### ax.plot_surface(x_plane, y_plane, z_plane, color='green', alpha=0.5)


plt.show()
