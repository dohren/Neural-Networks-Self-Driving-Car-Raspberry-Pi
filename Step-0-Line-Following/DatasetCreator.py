import ESP32camModule as wM
# import JoyStickModule as jsM
import KeyboardModule  as keyM
#import ESP32MotorModule as mM
import LineFollowingModule as lfM
import MqttMotorModule as mqtt
import cv2
from time import sleep
import time

maxThrottle = 0.5
motor = mqtt.Motor()

follow = 0
display = True

# Vorherige Werte initialisieren
prev_throttle = None
prev_steering = None

count = 0
last_time = time.time()

with open("C:\\workspace\\repos\\Neural-Networks-Self-Driving-Car-Raspberry-Pi\\Step-0-Line-Following\\pics\\inputs.txt", 'a') as testdata_file:

    while True:
        joyVal = keyM.getJS()

        direction = joyVal['axis1']
        steering = -joyVal['axis1']
        throttle = joyVal['axis2'] * -maxThrottle

        '''
        img = wM.getImg(display, size=[240, 120])
        if joyVal['options'] == 1:
            if follow == 0: print('Following Started ...')
            follow += 1
            sleep(0.300)
        if follow == 1:
            img = wM.getImg(display, size=[240, 120])
            result = lfM.follow(img, display)
            steering = -result['axis1'] * -maxThrottle
            throttle = result['axis2'] * -maxThrottle
        elif follow == 2:
            follow = 0
        '''

        current_time = time.time()
        if current_time - last_time >= 0.5:
            last_time = current_time
            wM.saveImg(str(count) + ".png")
            testdata_file.write(str(direction) + "\n")
            count += 1

        if throttle != prev_throttle or steering != prev_steering:
            motor.move(throttle, -steering, 0)
            print(f"SEND: throttle={throttle}, steering={steering}")
            prev_throttle = throttle
            prev_steering = steering

    