import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import hdbscan

# Load an image
image_path = "../thumbs2/T_978-2370840790.jpg"
img = Image.open(image_path)

# Convert the image to a NumPy array
data = np.array(img)

# Reshape the data to a 2D array where each row represents a pixel and its RGB values
data = data.reshape((-1, 3))

def find_optimal_clusters(data, max_clusters=10):
    distortions = []
    
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data.reshape(-1, data.shape[-1]))
        distortions.append(kmeans.inertia_)

    # Plot the elbow graph
    plt.plot(range(1, max_clusters + 1), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.title('Elbow Method for Optimal k')
    plt.show()

    # Find the optimal number of clusters based on the elbow
    optimal_clusters = np.argmin(np.diff(distortions)) + 1

    return optimal_clusters

# Apply K-means clustering
num_clusters = find_optimal_clusters(data)  # You can change this based on your dataset
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(data)

# Get cluster labels and cluster centers
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# Create a colored image where each pixel is assigned the color of its cluster center
clustered_image = centers[labels].reshape(img.size + (3,))

# Visualize the original and clustered images
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(img)
axes[0].set_title('Original Image')
axes[1].imshow(clustered_image.astype(np.uint8))
axes[1].set_title('Clustered Image')
plt.show()
