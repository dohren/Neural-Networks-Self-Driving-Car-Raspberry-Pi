import tensorflow as tf
from tensorflow.keras.mixed_precision import set_global_policy
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import os
from car_model import create_model
from car_data import binary_image_test_dataset



# Tensorflow GPU setup
print("Setup tensorflow...")
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)
set_global_policy('mixed_float16')



# Hyperparameter
input_image_width = 52
input_image_height = 52
input_image_channels = 1
input_dim = (input_image_width, input_image_height, input_image_channels)
output_dim = 2
dropout_rate = 0.2
noise = 0.1
learning_rate = 0.001
scale = 1

# Trainingssettings
batch_size = 256
iterations = 20
epochs = 10
checkpoint_interval = 5
save_dir = "model-trained"
os.makedirs(save_dir, exist_ok=True)

print("--- Hyperparameter ---")
print(f"input_dim = ({input_dim[0]}, {input_dim[1]}, {input_dim[2]})")
print(f"output_dim = ({output_dim})")
print(f"dropout_rate = {dropout_rate}")
print(f"noise = {noise}")
print(f"learning_rate = {learning_rate}")
print(f"scale = {scale}\n")

print("--- Trainings Settings ---")
print(f"batch_size = {batch_size}")
print(f"iterations = {iterations}")
print(f"epochs = {epochs}")
print(f"checkpoint_interval = {checkpoint_interval}\n")



print("Create model...")
model = create_model(input_dim, output_dim, dropout_rate, noise, learning_rate, scale)

print("Create datasets...")
dataset_training_input, dataset_training_output = binary_image_test_dataset(1000, (input_image_width, input_image_height), output_dim)
dataset_evaluation_input, dataset_evaluation_output = binary_image_test_dataset(1000, (input_image_width, input_image_height), output_dim)

print("Start training loop...")
best_eval_loss = float("inf")
history = {"accuracy": [], "loss": [], "val_accuracy": [], "val_loss": []}
for iteration in range(1, iterations + 1):
    # Fit an iteration
    print(f"Iteration {iteration}/{iterations}")
    model.fit(dataset_training_input, dataset_training_output, batch_size=batch_size, epochs=epochs, verbose=1)

    # Evaluate the model on the evaluation set
    eval_loss, eval_accuracy, eval_mae = model.evaluate(dataset_evaluation_input, dataset_evaluation_output, verbose=0)
    print(f"Evaluation - Loss: {eval_loss:.4f}, Accuracy: {eval_accuracy:.4f}, MAE: {eval_mae:.4f}")

    # Save history for plots
    history["accuracy"].append(eval_accuracy)
    history["loss"].append(eval_loss)
    history["val_accuracy"].append(eval_accuracy)
    history["val_loss"].append(eval_loss)

    # Checkpoint logic
    if iteration % checkpoint_interval == 0:
        print("Trainings checkpoint reached!")
        # Save best performance on evaluation set
        if eval_loss < best_eval_loss:
            print(f"Model improved with [Now: {eval_loss}, Before: {best_eval_loss}] and saved!")
            best_eval_loss = eval_loss
            model.save(os.path.join(save_dir, "model.h5"))
        else:
            print("Model did not improve, training discarded!")

print("Training finished!")

# Plot history
print("Create plots...")
plt.figure(figsize=(12, 6))

# Accuracy
plt.subplot(1, 2, 1)
plt.plot(history["accuracy"], label="Evaluation Accuracy")
plt.title("Accuracy Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid()

# Loss
plt.subplot(1, 2, 2)
plt.plot(history["loss"], label="Evaluation Loss")
plt.title("Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig(os.path.join(save_dir, "training_graphs.png"))
plt.show()

print("Load the trained model and run real predicitons...")
model = load_model(os.path.join(save_dir, "model.h5"))
predictions = model.predict(dataset_evaluation_input)
print("Real Predictions:")
for i in range(5):
    print(f"Prediction {i+1}: {predictions[i]}")

print("\nWe finished! Enjoy the model :3\n")


