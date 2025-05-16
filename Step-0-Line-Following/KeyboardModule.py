"""
-This module gets the arrow key values
and puts them in a single dictionary in real time.
-The values can be accessed through the keys
-Tested with keyboard only (no gamepad)
"""

import pygame
from time import sleep

pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Keyboard Joystick")

buttons = {
    'x': 0, 'o': 0, 't': 0, 's': 0,
    'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
    'share': 0, 'options': 0,
    'up': 0, 'down': 0, 'left': 0, 'right': 0,
    'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.
}

axis_state = {
    'x': 0.0,
    'y': 0.0
}

def getJS(name=''):
    global buttons, axis_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                buttons['up'] = 1
                axis_state['y'] = -1.0
            elif event.key == pygame.K_DOWN:
                buttons['down'] = 1
                axis_state['y'] = 1.0
            elif event.key == pygame.K_LEFT:
                buttons['left'] = 1
                axis_state['x'] = -1.0
            elif event.key == pygame.K_RIGHT:
                buttons['right'] = 1
                axis_state['x'] = 1.0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                buttons['up'] = 0
                axis_state['y'] = 0.0
            elif event.key == pygame.K_DOWN:
                buttons['down'] = 0
                axis_state['y'] = 0.0
            elif event.key == pygame.K_LEFT:
                buttons['left'] = 0
                axis_state['x'] = 0.0
            elif event.key == pygame.K_RIGHT:
                buttons['right'] = 0
                axis_state['x'] = 0.0

    buttons['axis1'] = axis_state['x']
    buttons['axis2'] = axis_state['y']
    buttons['axis3'] = 0.0
    buttons['axis4'] = 0.0

    return buttons if name == '' else buttons.get(name, None)


def main():
    print(getJS())         # All values
    sleep(0.05)
    print(getJS('right'))  # Single value example
    sleep(0.05)


if __name__ == '__main__':
    while True:
        main()
