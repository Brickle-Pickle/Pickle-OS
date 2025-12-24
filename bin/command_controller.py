# command_controller.py -> Command controller for the MiniPC.
import uos
from bin import ls, cd, cat, mkdir, rm, nano, sys, paint, bitlense
from system.config import BIG_DISPLAY

command_controller = {
    "ls": ls,
    "cd": cd,
    "cat": cat,
    "mkdir": mkdir,
    "rm": rm,
    "nano": nano,
    "sys": sys,
    "paint": paint,
    "bitlense": bitlense,
    "bt": bitlense,
}

def is_command(command):
    return command in command_controller

def execute_command(command, args):
    if is_command(command):
        getattr(command_controller[command], command)(args)
    else:
        return "X"

def get_command_help(command):
    if is_command(command):
        module = command_controller[command]
        if hasattr(module, "help"):
            module.help()
            BIG_DISPLAY.clear()
            BIG_DISPLAY.show()
            input_buffer["reset_keyboard"] = True
            input_buffer["reset_shell"] = True
            return
        else:
            BIG_DISPLAY.show_info(["No help available", "for " + command], 2)
            
    else:
        return "X"

def get_command_list():
    return command_controller.keys()