# cat.py -> Command to display the content of a file (available extensions: .txt, .py)

import time
from system.config import BIG_DISPLAY, SMALL_DISPLAY, BUTTON_LEFT, JOYSTICK
from system.shared_states import input_buffer

# Constants
CHAR_WIDTH = 8
LINES_ON_SCREEN = 6
BLOCK_SIZE = 256  # bytes per read (safe for MicroPython)

# Read lines chunk
def read_lines_chunk(f, num_chars, leftover=""):
    # Read a chunk of data from the file
    data = f.read(BLOCK_SIZE)
    if not data:
        if leftover:
            return [leftover], "", True
        return [], "", True  # EOF

    data = leftover + data
    lines = []

    while len(data) >= num_chars:
        lines.append(data[:num_chars])
        data = data[num_chars:]

    return lines, data, False

def cat(args):
    # Validate arguments
    if len(args) == 0:
        BIG_DISPLAY.show_info(["cat: no file", "to display"])
        return

    if len(args) > 1:
        BIG_DISPLAY.show_info(["cat: too many", "arguments"])
        return

    if not (args[0].endswith(".txt") or args[0].endswith(".py")):
        BIG_DISPLAY.show_info(["cat: invalid file", "extension"])
        return

    # Open the file
    try:
        with open(input_buffer["actual_path"] + "/" + args[0], "r") as f:

            num_chars = BIG_DISPLAY.get_width() // CHAR_WIDTH

            # State variables
            lines = []
            leftover = ""
            eof = False
            scroll_offset = 0
            changed = True
            in_command = True
            scroll_delay = 0.2

            # Initial load
            new_lines, leftover, eof = read_lines_chunk(f, num_chars)
            lines.extend(new_lines)

            if not lines:
                lines = [""]

            # Help display
            SMALL_DISPLAY.clear()
            SMALL_DISPLAY.text("Exit: Button Left", 0, 0)
            SMALL_DISPLAY.text("Scroll: Joystick", 0, 10)
            SMALL_DISPLAY.show()

            while in_command:
                # Load more data if needed
                if not eof and scroll_offset + LINES_ON_SCREEN >= len(lines):
                    new_lines, leftover, eof = read_lines_chunk(f, num_chars, leftover)
                    if new_lines:
                        lines.extend(new_lines)
                        changed = True

                # Update display if needed
                if changed:
                    changed = False
                    BIG_DISPLAY.clear()
                    for i in range(LINES_ON_SCREEN):
                        idx = scroll_offset + i
                        if idx < len(lines):
                            BIG_DISPLAY.text(lines[idx], 0, 10 + i * 10)
                    BIG_DISPLAY.show()

                # Exit
                if BUTTON_LEFT.is_pressed():
                    # Clear display and exit
                    BIG_DISPLAY.clear()
                    input_buffer["errased"] = True
                    input_buffer["reset_keyboard"] = True
                    input_buffer["reset_shell"] = True
                    in_command = False

                # Scroll
                direction = JOYSTICK.get_direction()
                if direction == "up":
                    if scroll_offset > 0:
                        scroll_offset -= 1
                        changed = True
                        time.sleep(scroll_delay)

                elif direction == "down":
                    if scroll_offset < len(lines) - LINES_ON_SCREEN:
                        scroll_offset += 1
                        changed = True
                        time.sleep(scroll_delay)
    except OSError:
        BIG_DISPLAY.show_info(["cat: no such", "file or directory"])
        return

def help():
    BIG_DISPLAY.show_info(["Usage:", "cat <filename>"], 4)
