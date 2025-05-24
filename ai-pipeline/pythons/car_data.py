import os
import numpy as np
import random
import cv2



# Load image from file
def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"No image found at: '{image_path}'")
    height, width = image.shape[:2]
    return image, width, height

# Convert image to black and white only (With threshold)
def process_image(image_data):
    gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    _, processed_black_white = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return processed_black_white

# Convert processed image to 1 (white pxiel) and 0 (black pixel)
def convert_image(image_processed):
    int_array = (image_processed == 255).astype(int)
    return int_array

# Int array to NP array
def binary_image_to_np_array(data):
    return np.array(data, dtype=np.float16)

# Image from path to np array
def image_path_to_np_array(image_path):
    image_data = load_image(image_path)
    image_processed = process_image(image_data)
    image_int_array = convert_image(image_processed)
    return binary_image_to_np_array(image_int_array)

# Image from data to np array
def image_data_to_np_array(image_data):
    image_processed = process_image(image_data)
    image_int_array = convert_image(image_processed)
    return binary_image_to_np_array(image_int_array)

# Load and convert all images from a directory, sorted numerically by filename (input samples)
def images_from_directory_to_np_array(image_dir):
    filenames = [f for f in os.listdir(image_dir) if f.lower().endswith(".jpg")]
    sorted_filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    image_arrays = []
    for fname in sorted_filenames:
        full_path = os.path.join(image_dir, fname)
        image_np = image_path_to_np_array(full_path).flatten()
        image_arrays.append(image_np)
    return np.array(image_arrays, dtype=np.float16)

# Read lines from .txt file and convert to np array (output samples)
def txtfile_to_np_array(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    float_values = [[np.float16(line.strip())] for line in lines if line.strip()]
    return np.array(float_values, dtype=np.float16)

# Create test dataset
def binary_image_test_dataset(samples=100, input_dim=(64, 64), output_dim=2):
    dataset_input = np.empty((samples, input_dim[0], input_dim[1]), dtype=np.float16)
    dataset_output = np.empty((samples, output_dim), dtype=np.float16)
    for i in range(samples):
        random_input_sample = [[random.randint(0, 1) for _ in range(input_dim[0])] for _ in range(input_dim[1])]
        random_output_sample = [random.randint(0, 1) for _ in range(output_dim)]
        dataset_input[i] = binary_image_to_np_array(random_input_sample)
        dataset_output[i] = binary_image_to_np_array(random_output_sample)
    return dataset_input, dataset_output

# Load real dataset
def binary_image_dataset(input_directory, output_file):
    dataset_input = images_from_directory_to_np_array(input_directory)
    dataset_output = txtfile_to_np_array(output_file)
    return dataset_input, dataset_output


