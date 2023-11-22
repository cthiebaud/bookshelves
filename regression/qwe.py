import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(42)
n_samples = 100
X1 = np.random.rand(n_samples)
X2 = np.random.rand(n_samples)
Y = 2 * X1 + 3 * X2 + np.random.randn(n_samples)

# Create a DataFrame
data = pd.DataFrame({'X1': X1, 'X2': X2, 'Y': Y})

# Fit the model
model = LinearRegression()
model.fit(data[['X1', 'X2']], data['Y'])

# Get the coefficients and intercept
beta1 = model.coef_[0]
beta2 = model.coef_[1]
beta0 = model.intercept_

# Create a meshgrid for the plane
X1_plane = np.linspace(X1.min(), X1.max(), 10)
X2_plane = np.linspace(X2.min(), X2.max(), 10)
X1_plane, X2_plane = np.meshgrid(X1_plane, X2_plane)
Y_plane = beta0 + beta1 * X1_plane + beta2 * X2_plane

# Plot the 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X1, X2, Y, c='r', marker='o')

# Plot the regression plane
ax.plot_surface(X1_plane, X2_plane, Y_plane, alpha=0.5)

# Set labels
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Y')

plt.show()
