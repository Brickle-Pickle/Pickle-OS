# mkdir.py -> Create a new directory
import uos
from system.config import BIG_DISPLAY

def mkdir(args):
    # Check if the number of arguments is correct
    if len(args) != 1:
        # Show an error message
        BIG_DISPLAY.show_error(["mkdir: too many", "arguments"])
        return

    # Get the directory name
    dir_name = args[0]
    
    try:
        # Create the directory
        uos.mkdir(dir_name)
        # Show a success message
        BIG_DISPLAY.show_error(["Directory: " + dir_name, "created"])
    except OSError:
        # Show an error message
        BIG_DISPLAY.show_error(["mkdir: directory", "already exists"])
        return
