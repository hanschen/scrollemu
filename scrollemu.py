#!/usr/bin/env python
"""Small utility that allows you to scroll by moving the mouse while holding
down a keyboard modifier key."""
import math

from pynput import mouse, keyboard
from pynput.keyboard import KeyCode
from pynput.mouse import Button


#
# OPTIONS
#

# Keyboard modifier key to hold down to start scrolling.
#
# Examples:
#   Key.cmd - Super/Windows/Command key
#   Key.ctrl - Ctrl key
#   Key.alt - Alt key
#   Key.shift - Shift key
#
# Add _l or _r to the end to specify only the left or right key.
#
# Default: Key.cmd_l
SCROLL_KEY = Button.button18

# Number of lines to scroll per pixels moved.
# Can be smaller than 1 but must be larger than 0.
#
# Default: 0.05
SENSITIVITY = 0.01

# Enable scrolling in vertical direction.
#
# Default: True
SCROLL_Y = True

# Enable scrolling in horizontal direction.
#
# Default: True
SCROLL_X = True

# Invert scrolling direction in vertical direction.
#
# Default: False
INVERT_Y = False

# Invert scrolling direction in horizontal direction.
#
# Default: False
INVERT_X = False

# Enable scroll acceleration (larger mouse movement -> more scrolling).
#
# Default: True
ACCELERATION = True


class ScrollEmu(object):
    def __init__(self):
        self.mouse = mouse.Controller()
        self.scroll_on = False
        self.mouse_displacement_x = 0
        self.mouse_displacement_y = 0
        self.mouse_lock_position = self.mouse.position

    @staticmethod
    def acceleration(displacement):
        """Return acceleration term based on displacement."""
        # A determines when the acceleration starts to kick into effect
        # (larger A -> more noticeable acceleration at smaller displacements)
        A = 0.0005

        # B controls the "steepness" of the acceleration curve
        # (larger B -> larger acceleration at larger displacements)
        B = 1.6

        return A * abs(displacement)**B

    def on_move(self, x, y):
        if not self.scroll_on:
            return

        lock_x, lock_y = self.mouse_lock_position

        # Do not do anything when resetting mouse position
        if x == lock_x and y == lock_y:
            return

        self.mouse.position = self.mouse_lock_position

        dy = y - lock_y
        dx = x - lock_x

        self.mouse_displacement_x = self.mouse_displacement_x + dx
        self.mouse_displacement_y = self.mouse_displacement_y + dy

        if SCROLL_Y and abs(self.mouse_displacement_y) >= 1./SENSITIVITY:
            self.scroll_y()

        if SCROLL_X and abs(self.mouse_displacement_x) >= 1./SENSITIVITY:
            self.scroll_x()

    def on_press(self, key):
        if key == SCROLL_KEY:
            self.scroll_on = True
            self.mouse_displacement_x = 0
            self.mouse_displacement_y = 0
            self.mouse_lock_position = self.mouse.position

    def on_release(self, key):
        if key == SCROLL_KEY:
            self.scroll_on = False

    def on_mousepress(self, x, y, button, pressed):
        if pressed and self.scroll_on:
            self.scroll_on = False
            return

        if pressed and button == SCROLL_KEY:
            self.scroll_on = True
            self.mouse_displacement_x = 0
            self.mouse_displacement_y = 0
            self.mouse_lock_position = self.mouse.position

    def scroll_lines(self, displacement, invert=False):
        """Return number of lines to scroll based on displacement."""
        scroll_lines = max([SENSITIVITY, 1])

        if ACCELERATION:
            acceleration = abs(self.acceleration(displacement))
            scroll_lines = scroll_lines + acceleration

        scroll_lines = math.copysign(scroll_lines, displacement)
        if invert:
            scroll_lines = -scroll_lines

        return scroll_lines

    def scroll_x(self):
        scroll_lines = self.scroll_lines(self.mouse_displacement_x, INVERT_X)
        self.mouse_displacement_x = 0
        self.mouse.scroll(scroll_lines, 0)

    def scroll_y(self):
        scroll_lines = self.scroll_lines(self.mouse_displacement_y, INVERT_Y)

        # Positive scroll = scroll down, need to reverse scroll direction
        scroll_lines = -scroll_lines

        self.mouse_displacement_y = 0
        self.mouse.scroll(0, scroll_lines)

    def run(self):
        mouse_listener = mouse.Listener(on_click=self.on_mousepress)
        mouse_listener.start()

        with mouse.Listener(on_move=self.on_move) as listener:
            listener.join()


if __name__ == "__main__":
    program = ScrollEmu()
    program.run()
