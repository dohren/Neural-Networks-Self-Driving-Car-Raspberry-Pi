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
    def __init__(self):
        self.cam_url = "http://192.168.8.186"
        # self.esp32_url = "http://192.168.8.189"
        self.esp32_url = "http://192.168.253.117"

    def move_cam(self, speed=0.5, turn=0, t=0.1):
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

        requests.get(self.cam_url + endpoint)
        sleep(t)

    def stop_cam(self, t=0):
        full_url = self.cam_url + '/stop'
        requests.get(full_url)
        sleep(t)

    def move_esp32(self, speed=0.5, turn=0, t=0):
        # Erstelle die URL mit den dynamischen Parametern
        endpoint = f"/move?speed={speed}&turn={turn}&t={t}"
        full_url = self.esp32_url + endpoint
        print(f"Anfrage: {full_url}")

        # HTTP GET-Anfrage senden
        requests.get(full_url)
        sleep(t)

    def stop_esp32(self, t=0):
        # Stop-Befehl senden
        full_url = self.esp32_url + "/move?speed=0&turn=0"
        print(f"Anfrage: {full_url}")
        
        requests.get(full_url)
        sleep(t)

    def move(self, speed=0.5, turn=0, t=0.1):
        self.move_esp32(speed, turn, t)

    def stop(self, t=0):
        self.stop_esp32(t)


def main():
    #motor.move(0.5,0,0.01)
    #motor.stop(2)
    #motor.move(-0.5,0,0.01)
    #motor.stop(2)
    #motor.move(1.3,1,1)
    #motor.stop(2)
    #motor.move(1.3,-1,1)
    #motor.stop(2)
    #motor.move(1.3,1,1)
    #motor.stop(2)
    #motor.move(1.3,-1,1)
    #motor.stop(2)
    motor.move(1.1,0,2)
    motor.stop(2)
    motor.move(-1.1,0,2)
    motor.stop(2)
    motor.move(0,1.1,2)
    motor.stop(2)
    motor.move(0,-1.1,2)
    motor.stop(2)



if __name__ == '__main__':
    motor= Motor()
    main()