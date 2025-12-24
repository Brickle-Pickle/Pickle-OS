# nano.py -> PickleOS nano text editor (read and write files)
import uos
import time
from system.config import SMALL_DISPLAY, BIG_DISPLAY, JOYSTICK
from bin.cat import cat
from system.keyboard import Keyboard
from system.shared_states import input_buffer

KEYBOARD = Keyboard()

def create_file(file):
    with open(file, "w") as f:
        f.write("")

def nano(args):
    readonly = "-r" in args
    if len(args) != 1 and not (len(args) == 2 and readonly):
        BIG_DISPLAY.show_error(["Usage error:"])
        BIG_DISPLAY.show_error(["nano [file] {-r}"])
        return

    file = None

    # If readonly, find the first non-option argument
    if not readonly:
        file = args[0]
    else:
        for arg in args:
            if not arg.startswith("-"):
                file = arg
                break

    file_name = ""
    if "." in file:
        file_name = file.split(".")[0] + ".txt"
    else:
        file_name = file + ".txt"

    file_path = input_buffer["actual_path"] + "/" + file_name

    # Check if the file exists, if not, create it
    try:
        uos.stat(file_path)
    except OSError:
        create_file(file_path)

    content = open_file(file_path, readonly, file_name)

    if content == "It is read-only":
        return

    SMALL_DISPLAY.clear()
    SMALL_DISPLAY.text("Save: Joy Button", 0, 0)
    SMALL_DISPLAY.text("Scroll: Joystick", 0, 10)
    SMALL_DISPLAY.text("Write/Del: BTNs", 0, 20)
    SMALL_DISPLAY.show()

    input_buffer["input"] = ""
    input_buffer["enter"] = False
    input_buffer["update_shell"] = False
    input_buffer["errased"] = False

    # Initialize cursor position and other state variables
    cursor_pos = len(content)
    needs_render = True
    cursor_state = True
    last_cursor_toggle = time.ticks_ms()
    scroll_offset = 0
    max_lines_on_screen = 8

    in_command = True
    while in_command:
        # If joystick button is pressed, save the file
        if JOYSTICK.is_button_pressed():
            in_command = False
            save_file(file_path, content)
            BIG_DISPLAY.show_error(["File saved"])
            input_buffer["errased"] = True
            input_buffer["reset_keyboard"] = True
            input_buffer["reset_shell"] = True
            time.sleep(1)
            return

        # Use a sentinel to reliably detect backspace from keyboard.py
        input_buffer["input"] = " "
        input_buffer["update_shell"] = False
        input_buffer["errased"] = False
        input_buffer["enter"] = False

        if KEYBOARD.read_input():
            time.sleep(0.2)

        # If modified, render the screen
        modified = False
        if input_buffer["update_shell"]:
            if input_buffer["errased"]:
                if cursor_pos > 0:
                    content = content[:cursor_pos - 1] + content[cursor_pos:]
                    cursor_pos -= 1
                    modified = True
            else:
                typed_chars = input_buffer["input"][1:]
                if typed_chars == "<":
                    cursor_pos = max(0, cursor_pos - 1)
                    modified = True
                elif typed_chars:
                    content = content[:cursor_pos] + typed_chars + content[cursor_pos:]
                    cursor_pos += len(typed_chars)
                    modified = True

        # If enter is pressed, move cursor to next line or add newline
        if input_buffer["enter"]:
            if KEYBOARD.flat_keyboard[KEYBOARD.actual_pos] == '>':
                cursor_pos = min(len(content), cursor_pos + 1)
            else:
                content = content[:cursor_pos] + '\n' + content[cursor_pos:]
                cursor_pos += 1
            modified = True

        if modified:
            needs_render = True
            lines_before_cursor = content[:cursor_pos].split('\n')
            current_line_index = len(lines_before_cursor) - 1
            if current_line_index < scroll_offset:
                scroll_offset = current_line_index
            if current_line_index >= scroll_offset + max_lines_on_screen:
                scroll_offset = current_line_index - max_lines_on_screen + 1

        if KEYBOARD.needs_render:
            KEYBOARD.display_keyboard()

        # Update cursor state
        if time.ticks_diff(time.ticks_ms(), last_cursor_toggle) > 500:
            cursor_state = not cursor_state
            last_cursor_toggle = time.ticks_ms()
            needs_render = True

        # Render the screen if needed
        if needs_render:
            BIG_DISPLAY.clear()
            lines = content.split('\n')
            display_lines = lines[scroll_offset : scroll_offset + max_lines_on_screen]
            y = 0
            for line in display_lines:
                BIG_DISPLAY.text(line[:21], 0, y)
                y += 8

            # Draw cursor if visible
            if cursor_state:
                lines_before_cursor = content[:cursor_pos].split('\n')
                current_line_index = len(lines_before_cursor) - 1
                if scroll_offset <= current_line_index < scroll_offset + max_lines_on_screen:
                    current_col = len(lines_before_cursor[-1])
                    y_pos = (current_line_index - scroll_offset) * 8
                    x_pos = current_col * 6
                    if x_pos > 122: x_pos = 122
                    BIG_DISPLAY.text("_", x_pos, y_pos)

            BIG_DISPLAY.show()
            needs_render = False

def save_file(file, content):
    with open(file, "w") as f:
        f.write(content)

def open_file(file_path, readonly, file_name):
    if not readonly:
        with open(file_path, "r") as f:
            return f.read()
    else:
        cat([file_name])
        return "It is read-only"