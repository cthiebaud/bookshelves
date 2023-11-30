from PIL import Image
import numpy as np
import sys

def shuffle_pixels(image_path, output_path):
    # Open the image
    original_image = Image.open(image_path)

    # Convert the image to a NumPy array
    pixel_array = np.array(original_image)

    # Reshape the array for shuffling
    height, width, channels = pixel_array.shape
    reshaped_array = pixel_array.reshape((-1, channels))

    # Shuffle the pixels
    np.random.shuffle(reshaped_array)

    # Reshape the shuffled array back to the original shape
    shuffled_array = reshaped_array.reshape((height, width, channels))

    # Create a new image from the shuffled array
    shuffled_image = Image.fromarray(shuffled_array, original_image.mode)

    # Save the shuffled image to the specified output path
    shuffled_image.save(output_path)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python shuffle_image.py input_image output_image")
        sys.exit(1)

    # Get input and output file paths from command line arguments
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    # Perform pixel shuffling and save the result
    shuffle_pixels(input_image_path, output_image_path)

    print(f"Pixel-shuffled image saved to {output_image_path}")

    