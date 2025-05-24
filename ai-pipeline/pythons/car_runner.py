import tensorflow as tf
from tensorflow.keras.mixed_precision import set_global_policy
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_custom_objects
from tensorflow.keras.layers import Layer
import numpy as np
import matplotlib.pyplot as plt
import os
from car_model import create_model
from car_data import image_data_to_np_array
import ESP32camModule as wM
import MqttMotorModule as mqtt
from time import sleep
import MqttMotorModule as mqtt


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

# H5 cusotm layer support
class Cast(Layer):
    def call(self, inputs):
        return tf.cast(inputs, tf.float16)
get_custom_objects().update({'Cast': Cast})



print("Load the trained model and run real predicitons...")
model_dir = "C:\model"
model = load_model(os.path.join(model_dir, "model.h5"))
motor = mqtt.Motor()

while True:
    # Übersetze Joystick Steuerung in Motor Steuerung
    vision_input = wM.getImg()
    processed_input = image_data_to_np_array(vision_input)

    prediction = model.predict(dataset_evaluation_input)
    steering = prediction[0] - prediction[1]
    if steering <= -0.5:
        steering = -1.0
    elif steering >= 0.5:
        steering = 1.0
    else:
        steering = 0

    throttle = 1.0

    # Moto Steuerung
    motor.move(throttle, steering, 0)


    