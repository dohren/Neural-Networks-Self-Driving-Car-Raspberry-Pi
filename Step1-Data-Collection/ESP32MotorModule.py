'''
-This module allows creation of robot objects for 2 or 4 wheeled robots.
-The motor driver used is the L298n.
-The base package used is the Rpi GPIO
-The Object Motor needs to be created first
-Then the move() function can be called to operate the motors
 move(speed,turn,delay)
-Speed and turn range from -1 to 1
-Delay is in seconds.
'''

import requests
from time import sleep

class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.url = "http://192.168.8.186"


    def move(self, speed=0.5, turn=0, t=0):
        if speed > 0 and turn == 0:
            endpoint = '/go'
        elif speed < 0 and turn == 0:
            endpoint = '/back' 
        elif speed == 0 and turn > 0:
            endpoint = '/left'
        elif speed == 0 and turn < 0:
            endpoint = '/right'
        else:
            endpoint = '/stop'

        full_url = self.url + endpoint
        response = requests.get(full_url)
        sleep(t)

    def stop(self, t=0):
        full_url = self.url + '/stop'
        response = requests.get(full_url)
        sleep(t)

def main():
    motor.move(0.5,0,0.05)
    motor.stop(2)
    motor.move(-0.5,0,0.05)
    motor.stop(2)
    motor.move(0,0.5,0.05)
    motor.stop(2)
    motor.move(0,-0.5,0.05)
    motor.stop(2)

if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27)
    main()