# cd.py -> Change directory command.
import uos
import time
from system.config import BIG_DISPLAY
from system.shared_states import input_buffer

def cd(args):
    # Check if the command has arguments
    if len(args) == 0:
        # Change to the root directory
        uos.chdir("/")
        input_buffer["actual_path"] = "/"
    elif len(args) > 1:
        # Show an error message
        BIG_DISPLAY.clear()
        BIG_DISPLAY.text("cd: too many", 0, 10)
        BIG_DISPLAY.text("arguments", 0, 20)
        BIG_DISPLAY.show()
        time.sleep(2)
        # Clear the error message
        BIG_DISPLAY.clear()
        input_buffer["errased"] = True
    elif args[0] == "..":
        # Change to the parent directory
        uos.chdir("..")
        input_buffer["actual_path"] = uos.getcwd()
        return
    else:
        # Change to the absolute path
        try:
            if args[0].startswith("/"):
                # Change to the absolute path
                uos.chdir(args[0])
            else:
                # Change to the relative path
                uos.chdir(input_buffer["actual_path"] + "/" + args[0])
        except:
            # Show an error message
            BIG_DISPLAY.clear()
            BIG_DISPLAY.text("cd: no such file", 0, 10)
            BIG_DISPLAY.text("or directory", 0, 20)
            BIG_DISPLAY.show()
            time.sleep(2)
            # Clear the error message
            BIG_DISPLAY.clear()
            input_buffer["errased"] = True
            return
        input_buffer["actual_path"] = uos.getcwd()
    
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show()
    input_buffer["reset_keyboard"] = True
    input_buffer["reset_shell"] = True