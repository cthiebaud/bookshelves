import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import hdbscan

def cluster_image(image_path, min_cluster_size = 50):
    # Load an image
    img = Image.open(image_path)

    # Convert the image to a NumPy array
    data = np.array(img)

    # Apply HDBSCAN clustering
    data_3d = data.reshape(-1, data.shape[-1])
    clusterer = hdbscan.HDBSCAN(min_cluster_size)
    labels = clusterer.fit_predict(data_3d)
    
    # Reshape the labels back to the shape of the image
    labels_2d = labels.reshape(img.size[0], img.size[1])

    # Print information about the clustering
    num_clusters = len(np.unique(labels)) - 1  # Exclude noise points (-1)
    noise_points = np.sum(labels == -1)
    print(f"Number of clusters: {num_clusters}")
    print(f"Number of noise points: {noise_points}")

    # Visualize the original and clustered images
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(img)
    axes[0].set_title('Original Image')

    cluster_img = axes[1].imshow(labels_2d, cmap='viridis')
    axes[1].set_title('HDBSCAN Clusters')

    # Display colorbar for the clustered image
    cbar = fig.colorbar(cluster_img, ax=axes[1])
    cbar.set_label('Cluster Label')

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hdbsca.py <min_cluster_size> <isbn>")
        sys.exit(1)

    min_cluster_size = int(sys.argv[1])
    image_path = f"../thumbs2/T_{sys.argv[2]}.jpg"
    cluster_image(image_path, min_cluster_size)
