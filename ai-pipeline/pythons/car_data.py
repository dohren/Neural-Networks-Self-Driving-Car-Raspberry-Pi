import numpy as np
import random



# Tensorflow GPU setup
def binary_image_to_np_array(data):
    return np.array(data, dtype=np.float16)

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


