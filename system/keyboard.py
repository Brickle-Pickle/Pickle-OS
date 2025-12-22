# keyboard.py -> Keyboard interface for the MiniPC.
from system.config import BUTTON_LEFT, BUTTON_RIGHT, JOYSTICK, SMALL_DISPLAY
from system.shared_states import input_buffer

# Keyboard interface
class Keyboard:
    def __init__(self):
        self.actual_pos = 0
        self.needs_render = True
        self.keyboard_map = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "."],
            ["Z", "X", "C", "V", "B", "N", "M", " ", "-", ">"]
        ]
        self.flat_keyboard = [letter for row in self.keyboard_map for letter in row]
        self.row_lengths = [len(row) for row in self.keyboard_map]
        self.row_starts = [0] * len(self.keyboard_map)
        for i in range(1, len(self.keyboard_map)):
            self.row_starts[i] = self.row_starts[i-1] + self.row_lengths[i-1]

    def display_keyboard(self):
        SMALL_DISPLAY.clear()
        pos_y = 0
        for row_idx, row in enumerate(self.keyboard_map):
            pos_x = 0
            for col_idx, letter in enumerate(row):
                index = self.row_starts[row_idx] + col_idx
                inverted_colors = (index == self.actual_pos)
                SMALL_DISPLAY.set_text_size(2)
                SMALL_DISPLAY.text(letter, pos_x, pos_y, "inverted" if inverted_colors else 1)
                pos_x += 12
            pos_y += 10
        SMALL_DISPLAY.show()
        self.needs_render = False

    def read_input(self):
        # Joystick values
        x_value, y_value = JOYSTICK.get_position()

        # Joystick left
        if x_value < 1000:
            self.actual_pos = max(0, self.actual_pos - 1)
            self.needs_render = True
            return True
        # Joystick right
        elif x_value > 60000:
            self.actual_pos = min(len(self.flat_keyboard) - 1, self.actual_pos + 1)
            self.needs_render = True
            return True
        # Joystick up
        elif y_value < 1000:
            self.actual_pos = max(0, self.actual_pos - self.row_lengths[0])
            self.needs_render = True
            return True
        # Joystick down
        elif y_value > 60000:
            self.actual_pos = min(len(self.flat_keyboard) - 1, self.actual_pos + self.row_lengths[0])
            self.needs_render = True
            return True

        # Button pressed
        if BUTTON_RIGHT.is_pressed():
            actual_letter = self.flat_keyboard[self.actual_pos]
            if actual_letter != ">":
                input_buffer["input"] += actual_letter
                input_buffer["update_shell"] = True
            else:
                input_buffer["enter"] = True
            self.needs_render = True
            return True

        if BUTTON_LEFT.is_pressed():
            print("Button left pressed")
            if input_buffer["input"]:
                # Remove last letter
                input_buffer["input"] = input_buffer["input"][:-1]
                input_buffer["update_shell"] = True
                input_buffer["errased"] = True
            self.needs_render = True
            return True
        
        return False