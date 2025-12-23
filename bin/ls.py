# ls.py -> List directory contents.
import uos
import time
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY, SMALL_DISPLAY, BUTTON_LEFT, JOYSTICK

MAX_FILES = 5

def ls():
    in_command = True

    files = uos.listdir()
    file_index = 0
    file_count = len(files)
    max_file_index = file_count - MAX_FILES # k-MAX_FILES because we want to show MAX_FILES files at a time (first file is at index 0)

    SMALL_DISPLAY.clear()
    SMALL_DISPLAY.set_text_size(1)
    SMALL_DISPLAY.text("ls:", 0, 0)
    SMALL_DISPLAY.text("Press left", 0, 10)
    SMALL_DISPLAY.text("to exit", 0, 20)
    SMALL_DISPLAY.show()

    print_active_files(files, file_index)

    while in_command:
        # Check if left button was pressed to exit
        if BUTTON_LEFT.is_pressed():
            in_command = False
            BIG_DISPLAY.clear()
            BIG_DISPLAY.show()
            input_buffer["reset_keyboard"] = True
            input_buffer["reset_shell"] = True
        
        if in_command:
            direction = JOYSTICK.get_direction()
            if direction == "left" or direction == "up":
                time.sleep(0.2)
                # Move left or up, but not past the first file
                file_index = max(0, file_index - 1)
                file_index = print_active_files(files, file_index)
            elif direction == "right" or direction == "down":
                time.sleep(0.2)
                # Move right or down, but not past the last file
                file_index = min(max_file_index, file_index + 1)
                file_index = print_active_files(files, file_index)

def print_active_files(files, file_index):
    # Clear the display
    BIG_DISPLAY.clear()

    # Print the active files
    for i, file in enumerate(files[file_index:file_index+MAX_FILES]):
        BIG_DISPLAY.text(file if "." in file else file + "/", 0, i * 10)
        BIG_DISPLAY.show()

    return file_index