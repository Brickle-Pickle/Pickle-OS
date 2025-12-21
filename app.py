# app.py -> Primary application logic.
import time
import _thread
from system.shell import Shell
from system.keyboard import Keyboard

print("Initializing shell and keyboard...")
SHELL = Shell("root") # For now, only root user is supported (TODO: Add user support)
KEYBOARD = Keyboard()

# Start the shell in a separate thread
print("Starting shell thread...")
_thread.start_new_thread(SHELL.run, ())

# Run the keyboard listener in the main thread
# This will block and keep the program running
print("Starting keyboard listener...")

KEYBOARD.run()