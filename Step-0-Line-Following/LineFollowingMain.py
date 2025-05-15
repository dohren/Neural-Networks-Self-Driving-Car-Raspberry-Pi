import ESP32camModule as wM
# import JoyStickModule as jsM
import KeyboardModule  as keyM
#import ESP32MotorModule as mM
import LineFollowingModule as lfM
import MqttMotorModule as mqtt
import cv2
from time import sleep

maxThrottle = 1
motor = mqtt.Motor()

follow = 0
display = True

# Vorherige Werte initialisieren
prev_throttle = None
prev_steering = None

while True:
    joyVal = keyM.getJS()
    steering = -joyVal['axis1']
    throttle = joyVal['axis2'] * -maxThrottle

    if joyVal['options'] == 1:
        if follow == 0: print('Following Started ...')
        follow += 1
        sleep(0.300)
    if follow == 1:
        img = wM.getImg(display, size=[240, 120])
        result = lfM.follow(img, display)
        steering = -result['axis1']
        throttle = result['axis2'] * -maxThrottle
    elif follow == 2:
        follow = 0

    time = 0.2
    if steering != 0:
        time = 0.15

    # Sende nur, wenn sich throttle oder steering geändert haben
    if throttle != prev_throttle or steering != prev_steering:
        motor.move(throttle, -steering, time)
        print(f"SEND: throttle={throttle}, steering={steering}")
        prev_throttle = throttle
        prev_steering = steering

    