# keyboard.py -> Keyboard interface for the MiniPC.
from system.config import BUTTON_LEFT, BUTTON_RIGHT, JOYSTICK, SMALL_DISPLAY
from system.shared_states import input_buffer
import time

STANDARD_WAIT_TIME = 0.3

# Keyboard interface
class Keyboard:
    def __init__(self):
        self.actual_pos = 0
        self.keyboard_map = { 
            "row_0": { "Q": 0, "W": 1, "E": 2, "R": 3, "T": 4, "Y": 5, "U": 6, "I": 7, "O": 8 },
            "row_1": { "A": 9, "S": 10, "D": 11, "F": 12, "G": 13, "H": 14, "J": 15, "K": 16, "L": 17 },
            "row_2": { "Z": 18, "X": 19, "C": 20, "V": 21, "B": 22, "N": 23, "M": 24, "P": 25, ">": 26 }
        }
        self.letter_map = [
            "Q", "W", "E", "R", "T", "Y", "U", "I", "O",
            "A", "S", "D", "F", "G", "H", "J", "K", "L",
            "Z", "X", "C", "V", "B", "N", "M", "P", ">"
        ]

    def display_keyboard(self):
        SMALL_DISPLAY.clear()
        pos_y = 0
        for row in self.keyboard_map.values():
            pos_x = 0
            for letter, index in row.items():
                inverted_colors = (index == self.actual_pos)
                SMALL_DISPLAY.text(letter, pos_x, pos_y, "inverted" if inverted_colors else 1)
                pos_x += 7
            pos_y += 8
        SMALL_DISPLAY.show()

    def read(self):
        self.display_keyboard()
        
        # Joystick left
        if JOYSTICK.is_left():
            if self.actual_pos > 0:
                if self.actual_pos != 9 and self.actual_pos != 18:
                    self.actual_pos -= 1
                else:
                    self.actual_pos -= 9
            else:
                self.actual_pos = 27
            
            self.display_keyboard()
            time.sleep(STANDARD_WAIT_TIME)
        # Joystick right
        if JOYSTICK.is_right():
            if self.actual_pos < 27:
                if self.actual_pos != 8 and self.actual_pos != 17:
                    self.actual_pos += 1
                else:
                    self.actual_pos += 9
            else:
                self.actual_pos = 0
            
            self.display_keyboard()
            time.sleep(STANDARD_WAIT_TIME)
        # Joystick up
        if JOYSTICK.is_up():
            if self.actual_pos > 8:
                self.actual_pos -= 9
            else:
                self.actual_pos += 18
            
            self.display_keyboard()
            time.sleep(STANDARD_WAIT_TIME)
        # Joystick down
        if JOYSTICK.is_down():
            if self.actual_pos < 18:
                self.actual_pos += 9
            else:
                self.actual_pos -= 18
            
            self.display_keyboard()
            time.sleep(STANDARD_WAIT_TIME)

        # Button pressed
        if BUTTON_RIGHT.is_pressed():
            actual_letter = self.letter_map[self.actual_pos]
            if actual_letter != ">":
                input_buffer["input"] += actual_letter
                self.display_keyboard()
                time.sleep(STANDARD_WAIT_TIME)
            else:
                input_buffer["enter"] = True
                self.display_keyboard()
                time.sleep(STANDARD_WAIT_TIME)

        if BUTTON_LEFT.is_pressed():
            if input_buffer["input"]:
                input_buffer["input"] = input_buffer["input"][:-1]
                self.display_keyboard()
                time.sleep(STANDARD_WAIT_TIME)

    def run(self):
        print("Keyboard is running...")
        while True:
            self.read()