# bitlense.py -> Viewer for .bitimg files
from system.config import BIG_DISPLAY, JOYSTICK
from system.shared_states import input_buffer
import time

def bitlense(args):
    if len(args) != 1:
        BIG_DISPLAY.show_info(["Usage:", "bitlense <file>"], 2)
        return

    filename = (args[0] if "." not in args[0] else args[0].split(".")[0]) + ".bitimg"
    
    pixel_map = load_map(filename)
    
    if not pixel_map:
        BIG_DISPLAY.show_info(["Error:", "File not found", "or invalid"], 2)
        return

    show_viewer(filename, pixel_map)

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
    except:
        return None

def show_viewer(filename, pixel_map):
    BIG_DISPLAY.clear()
    
    # Draw image
    # We access .display directly for pixel manipulation
    for x in range(128):
        for y in range(64):
            if pixel_map[x][y]:
                BIG_DISPLAY.display.pixel(x, y, 1)
    BIG_DISPLAY.show()
    
    # Wait for exit
    viewing = True
    while viewing:
        if JOYSTICK.is_button_pressed():
            viewing = False
            # Reset shell state
            input_buffer["input"] = " "
            input_buffer["update_shell"] = False
            input_buffer["errased"] = True
            input_buffer["enter"] = False
        time.sleep(0.1)

def help():
    BIG_DISPLAY.show_info(["Usage:", "bitlense <file>"], 2)
    BIG_DISPLAY.show_info(["Desc:", "View .bitimg files"], 2)