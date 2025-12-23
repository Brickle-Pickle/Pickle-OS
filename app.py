# app.py -> Primary application logic.
import time
from system.shell import Shell
from system.keyboard import Keyboard
from system.shared_states import input_buffer

print("Initializing shell and keyboard...")
SHELL = Shell("root") # For now, only root user is supported (TODO: Add user support)
KEYBOARD = Keyboard()

while True:
    # Check for user input
    if (KEYBOARD.read_input()):
        # If a key was pressed, wait a bit to avoid double presses
        time.sleep(0.2)

    # Check if keyboard needs to be rendered
    if KEYBOARD.needs_render:
        KEYBOARD.display_keyboard()

    # Check if enter was pressed
    if input_buffer["enter"]:
        SHELL.display_prompt()
        command = input_buffer["input"]
        input_buffer["enter"] = False
        input_buffer["input"] = ""
        SHELL.history.append(command)
        SHELL.history_index = len(SHELL.history)
        SHELL.execute(command)

    # Check if shell needs to be updated
    if input_buffer["update_shell"] or input_buffer["reset_shell"]:
        input_buffer["update_shell"] = False
        SHELL.prompt = SHELL.user + input_buffer["input"]
        SHELL.display_prompt()

    if input_buffer["reset_keyboard"]:
        input_buffer["reset_keyboard"] = False
        KEYBOARD.display_keyboard()