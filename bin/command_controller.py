# command_controller.py -> Command controller for the MiniPC.
import uos
from bin import ls, cd, cat

command_controller = {
    "ls": ls.ls,
    "cd": cd.cd,
    "cat": cat.cat,
}

def is_command(command):
    return command in command_controller

def execute_command(command, args):
    if is_command(command):
                command_controller[command](args)
    else:
        return "X"

def get_command_help(command):
    if is_command(command):
        return command_controller[command].help()
    else:
        return "X"

def get_command_list():
    return command_controller.keys()