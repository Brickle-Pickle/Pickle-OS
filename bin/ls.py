# ls.py -> List directory contents.
import uos
import time
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY, SMALL_DISPLAY, BUTTON_LEFT, JOYSTICK

MAX_FILES = 5

def ls(args):
    in_command = True
    detailed = False
    only_directory = False
    only_files = False

    path = None
    if len(args) > 0:
        for arg in args:
            if arg == "-l":
                detailed = True
            elif arg == "-d" and not only_files:
                only_directory = True
            elif arg == "-f" and not only_directory:
                only_files = True
            else:
                # If the argument doesn't start with a "-", may be a path
                if "-" not in arg:
                    path = arg
                    if path.startswith("/"):
                        path = path[1:]
                    
                    # Verify if the path exists
                    try:
                        uos.stat(path)
                    except OSError:
                        path = None
    
    files = uos.listdir(path if path else input_buffer["actual_path"])

    # Filter the files
    if only_directory:
        files = [file for file in files if "." not in file]
    elif only_files:
        files = [file for file in files if "." in file]

    # Format the files with detailed information (size)
    if detailed:
        new_files = []
        for file in files:
            stat = uos.stat(file)
            size = stat[6]
            new_files.append(file if "." in file else file + "/" + " | " + str(size)) 
        files = new_files
    
    # Print the files
    file_index = 0
    file_count = len(files)
    max_file_index = file_count - MAX_FILES # k-MAX_FILES because we want to show MAX_FILES files at a time (first file is at index 0)

    SMALL_DISPLAY.clear()
    SMALL_DISPLAY.set_text_size(1)
    SMALL_DISPLAY.text("ls:", 0, 0)
    SMALL_DISPLAY.text("Press left", 0, 10)
    SMALL_DISPLAY.text("to exit", 0, 20)
    SMALL_DISPLAY.show()

    print_active_files(files, file_index, detailed)

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
                file_index = print_active_files(files, file_index, detailed)
            elif direction == "right" or direction == "down":
                time.sleep(0.2)
                # Move right or down, but not past the last file
                file_index = min(max_file_index, file_index + 1)
                file_index = print_active_files(files, file_index, detailed)

def print_active_files(files, file_index, detailed):
    # Clear the display
    BIG_DISPLAY.clear()

    # Print the active files
    for i, file in enumerate(files[file_index:file_index+MAX_FILES]):
        BIG_DISPLAY.text(file if "." in file or detailed else file + "/", 0, i * 10)
        BIG_DISPLAY.show()

    return file_index

def help():
    BIG_DISPLAY.show_info(["Usage: ls [path]", "[-l] [-d] [-f]"], 4)