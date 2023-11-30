import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_3d_spiral(num_points, height_factor=1, base_radius_factor=1, height_exponent=1, radius_exponent=1, some_other_parameter=1, num_rotations=1):
    theta = np.linspace(0, 2 * np.pi * num_rotations, num_points)
    z = height_factor * np.exp(height_exponent * theta / (2 * np.pi * num_rotations))
    radius_factor = base_radius_factor * np.exp((radius_exponent ** some_other_parameter) * theta / (2 * np.pi * num_rotations))

    x = radius_factor * np.cos(theta)
    y = radius_factor * np.sin(theta)

    return x, y, z

def plot_3d_spiral(num_points=100, height_factor=1, base_radius_factor=1, height_exponent=1, radius_exponent=1, some_other_parameter=1, num_rotations=1):
    x, y, z = generate_3d_spiral(num_points, height_factor, base_radius_factor, height_exponent, radius_exponent, some_other_parameter, num_rotations)

    # Scale and translate the coordinates to fit into [0, 255] cube
    x = (x - np.min(x)) / (np.max(x) - np.min(x)) * 255
    y = (y - np.min(y)) / (np.max(y) - np.min(y)) * 255
    z = (z - np.min(z)) / (np.max(z) - np.min(z)) * 255

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label=f'3D Spiral (Exponential Radius and Height with Parameter)')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    plt.show()

# Demo: Plot a 3D spiral with exponentially increasing radius and height with a parameter
plot_3d_spiral(40000, height_factor=.1, base_radius_factor=.1, height_exponent=2, radius_exponent=2, some_other_parameter=3, num_rotations=20)
