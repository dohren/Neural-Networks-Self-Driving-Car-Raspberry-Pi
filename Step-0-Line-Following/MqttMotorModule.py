'''
-This module allows creation of robot objects for 2 or 4 wheeled robots.
-The control is sent via MQTT.
-The MQTT topic is 'robot1/motor/control'.
-The broker address is 'lumabit-laptop-01'.
-The move() function can be called to operate the motors.
 move(speed,turn,delay)
-Speed and turn range from -1 to 1
-Delay is in seconds.
'''

import time
import json
import paho.mqtt.client as mqtt

class Motor:
    def __init__(self):
        self.broker = "lumabit-laptop-01.local"
        self.port = 1883
        self.topic = "robot1/motor/control"

        self.client = mqtt.Client()
        self.client.connect(self.broker, self.port)

    def move(self, speed=0.5, turn=0, t=0.1):
        command = {
            "speed": speed,
            "turn": turn
        }
        self.client.publish(self.topic, json.dumps(command))


    def stop(self, t=0):
        command = {
            "speed": 0,
            "turn": 0
        }
        self.client.publish(self.topic, json.dumps(command))

def main():
    motor.move(1.1, 0, 2)
    motor.stop(2)
    motor.move(-1.1, 0, 2)
    motor.stop(2)
    motor.move(0, 1.1, 2)
    motor.stop(2)
    motor.move(0, -1.1, 2)
    motor.stop(2)

if __name__ == '__main__':
    motor = Motor()
    main()
