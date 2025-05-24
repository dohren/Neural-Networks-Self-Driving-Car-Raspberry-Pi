import ESP32camModule as wM
import KeyboardModule  as keyM
import MqttMotorModule as mqtt
from time import sleep
import time

maxThrottle = 0.5
motor = mqtt.Motor()

# Millisekunden bis ein neues Sample recorded wird
record_intervall = 500.0

# Trigger und utility
prev_throttle = 0
prev_steering = 0
count = 0
last_time = time.time()

with open("C:\\workspace\\repos\\Neural-Networks-Self-Driving-Car-Raspberry-Pi\\Step-0-Line-Following\\pics\\inputs.txt", 'a') as testdata_file:

    while True:
        # Get Steuerung Inputs
        joyVal = keyM.getJS()

        # Übersetze Joystick Steuerung in Motor Steuerung
        steering = -joyVal['axis1']
        throttle = joyVal['axis2'] * -maxThrottle

        # Überprüfung ob ein neues Sample aufgenommen werden soll
        current_time = time.time()
        if current_time - last_time >= record_intervall:
            last_time = current_time
            wM.saveImg(str(count) + ".png")
            testdata_file.write(str(-steering) + "\n")
            count += 1
        
        # Moto Steuerung
        if throttle != prev_throttle or steering != prev_steering:
            motor.move(throttle, -steering, 0)
            prev_throttle = throttle
            prev_steering = steering
