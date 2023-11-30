import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generate_uniform_points_on_sphere_surface(num_points):
    # Azimuthal angle (horizontal): Ranges from 0 to 2π
    theta = np.linspace(0, 2 * np.pi, num_points)

    # Polar angle (vertical): Ranges from 0 to π
    phi = np.linspace(0, np.pi, num_points)

    # Create a meshgrid of azimuthal and polar angles
    theta, phi = np.meshgrid(theta, phi)

    # Convert spherical coordinates to Cartesian coordinates
    x = np.sin(phi) * np.cos(theta)  # Possible range: [-1, 1]
    y = np.sin(phi) * np.sin(theta)  # Possible range: [-1, 1]
    z = np.cos(phi)                  # Possible range: [-1, 1]

    # Combine x, y, and z to form the 3D points on the sphere's surface
    points = np.column_stack((x.flatten(), y.flatten(), z.flatten()))

    return points

# Define the desired width and calculate the corresponding height based on the golden ratio
num_points = (2*2)*(3*3)
width = (2*2)*(3*3)
height = (2*2)*(3*3)

# Generate uniform RGB values for each pixel on the surface of the sphere
points_on_sphere_surface = generate_uniform_points_on_sphere_surface(num_points)

colors_on_sphere_surface = (points_on_sphere_surface + 1) / 2  # Map coordinates to RGB range [0, 1]

boh = colors_on_sphere_surface.reshape(width, height, 3)
# Shuffle the pixels randomly
## np.random.shuffle(boh)
print("boh boh boh")
print(boh.shape, boh)

# Normalize coordinates to the range [0, 255]
points = (boh * 255).astype(np.uint8)
print("points points points")
print(points.shape, points)

# Reshape 
points2 = points.reshape(-1, 3)

points3 = np.tile(points2, (9, 1))
# shuffle
## np.random.shuffle(points2)

# shuffle
points4 = points3.reshape(width*3, height*3, 3)

# Convert the array to an image
image = Image.fromarray(points4, 'RGB')

# Save the image
image.save('sphere_image_surface_uniform.png')


#### # Save the pixels on the surface as an image
#### plt.imsave('sphere_image_surface_uniform4.jpg', boh)
#### 
#### # Create a 3D scatter plot
#### fig = plt.figure()
#### ax = fig.add_subplot(111, projection='3d')
#### 
#### # Plot the 3D scatter plot
#### ax.scatter(points_on_sphere_surface[:, 0], points_on_sphere_surface[:, 1], points_on_sphere_surface[:, 2], c=colors_on_sphere_surface)
#### 
#### # Set axis labels
#### ax.set_xlabel('Red')
#### ax.set_ylabel('Green')
#### ax.set_zlabel('Blue')
#### 
#### plt.show()
#### 