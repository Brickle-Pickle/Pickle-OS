# paint.py -> Paint program for the MiniPC. Bit a bit, creates in .bitimg files.
from system.config import BIG_DISPLAY, JOYSTICK, BUTTON_LEFT, BUTTON_RIGHT
from system.shared_states import input_buffer
import time

def paint(args):
    if len(args) != 1:
        BIG_DISPLAY.show_info(["Usage:", "paint <filename>"], 2)
        return

    filename = (args[0] if "." not in args[0] else args[0].split(".")[0]) + ".bitimg"
    
    # Try to load existing map or create new one
    pixel_map = load_map(filename)
    if not pixel_map:
        # Create new 128x64 map (initialized to 0)
        pixel_map = [[0 for _ in range(64)] for _ in range(128)]

    paint_editor(filename, pixel_map)

def load_map(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            new_map = [[0 for _ in range(64)] for _ in range(128)]
            for y, line in enumerate(lines):
                line = line.strip()
                for x, char in enumerate(line):
                    if x < 128 and y < 64:
                        new_map[x][y] = int(char)
            return new_map
    except OSError:
        return None

def save_map(filename, pixel_map):
    try:
        with open(filename, "w") as f:
            for y in range(64):
                line = ""
                for x in range(128):
                    line += str(pixel_map[x][y])
                f.write(line + "\n")
        return True
    except:
        return False

def paint_editor(filename, pixel_map):
    # Instructions
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Paint v0.1", 0, 0)
    BIG_DISPLAY.text("L-BTN: Erase", 0, 15)
    BIG_DISPLAY.text("R-BTN: Paint", 0, 25)
    BIG_DISPLAY.text("JOY-BTN: Save", 0, 35)
    BIG_DISPLAY.show()
    time.sleep(2)
    
    BIG_DISPLAY.clear()
    
    # Initial Draw
    # We access .display directly for pixel manipulation
    for x in range(128):
        for y in range(64):
            if pixel_map[x][y]:
                BIG_DISPLAY.display.pixel(x, y, 1)
    BIG_DISPLAY.show()

    painting = True
    cursor_x, cursor_y = 64, 32
    cursor_state = True
    last_cursor_time = time.ticks_ms()
    
    while painting:
        # Cursor Blinking Logic
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_cursor_time) > 300:
            cursor_state = not cursor_state
            last_cursor_time = current_time
            # Draw cursor (inverted pixel)
            current_color = pixel_map[cursor_x][cursor_y]
            display_color = 0 if (cursor_state and current_color) else 1 if cursor_state else current_color
            BIG_DISPLAY.display.pixel(cursor_x, cursor_y, display_color)
            BIG_DISPLAY.show()

        # Movement
        direction = JOYSTICK.get_direction()
        moved = False
        prev_x, prev_y = cursor_x, cursor_y
        
        if direction == "up" and cursor_y > 0:
            cursor_y -= 1
            moved = True
        elif direction == "down" and cursor_y < 63:
            cursor_y += 1
            moved = True
        elif direction == "left" and cursor_x > 0:
            cursor_x -= 1
            moved = True
        elif direction == "right" and cursor_x < 127:
            cursor_x += 1
            moved = True
            
        if moved:
            # Restore pixel at old position
            BIG_DISPLAY.display.pixel(prev_x, prev_y, pixel_map[prev_x][prev_y])
            # Cursor will be drawn in next blink cycle or immediately for responsiveness
            cursor_state = True
            last_cursor_time = time.ticks_ms() - 301 # Force immediate update
            
        # Painting / Erasing
        if BUTTON_RIGHT.is_pressed(): # Paint
            pixel_map[cursor_x][cursor_y] = 1
            BIG_DISPLAY.display.pixel(cursor_x, cursor_y, 1)
            BIG_DISPLAY.show()
            
        if BUTTON_LEFT.is_pressed(): # Erase
            pixel_map[cursor_x][cursor_y] = 0
            BIG_DISPLAY.display.pixel(cursor_x, cursor_y, 0)
            BIG_DISPLAY.show()

        # Save and Exit
        if JOYSTICK.is_button_pressed():
            BIG_DISPLAY.clear()
            BIG_DISPLAY.show_info(["Saving..."])
            if save_map(filename, pixel_map):
                BIG_DISPLAY.show_info(["Saved:", filename], 2)
            else:
                BIG_DISPLAY.show_info(["Error saving"], 2)
            
            painting = False
            # Reset shell state
            input_buffer["input"] = " "
            input_buffer["update_shell"] = False
            input_buffer["errased"] = True
            input_buffer["enter"] = False
            
        time.sleep(0.05) # Prevent CPU hogging

def help():
    BIG_DISPLAY.show_info(["Usage:", "paint <file>"], 2)
    BIG_DISPLAY.show_info(["Desc:", "Pixel art editor"], 2)