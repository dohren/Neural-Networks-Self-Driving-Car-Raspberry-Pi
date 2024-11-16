import ESP32camModule as wM
import JoyStickModule as jsM
import ESP32MotorModule as mM
import LineFollowingModule as lfM
import cv2
from time import sleep


maxThrottle = 1.5
motor = mM.Motor()

follow = 0
display = True

while True:
    joyVal = jsM.getJS()
    steering = joyVal['axis1']
    throttle = joyVal['axis2']*-maxThrottle
    if joyVal['options'] == 1:
        if follow ==0: print('Following Started ...')
        follow +=1
        sleep(0.300)
    if follow == 1:
        img = wM.getImg(display, size=[240,120])
        result = lfM.follow(img, display)
        steering = result['axis1']
        throttle = result['axis2']*-maxThrottle
    elif follow == 2:
        follow = 0

    # print(throttle)
    motor.move(throttle,-steering)
    cv2.waitKey(2)