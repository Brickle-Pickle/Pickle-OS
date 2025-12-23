# shell.py -> Shell interface for the MiniPC.
import uos
import time
from bin import command_controller
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY

class Shell:
    def __init__(self, user):
        self.user = user + "> "
        self.current_dir = "/"
        self.running = True
        self.history = []
        self.history_index = 0
        self.history_max = 10
        self.prompt = self.user
        self.display_prompt()

    def display_prompt(self):
        if input_buffer["errased"]:
            BIG_DISPLAY.clear()
            input_buffer["errased"] = False
        
        BIG_DISPLAY.text(self.prompt, 0, 10)

        # Verify if the prompt is too long to fit in the display and print it in separate lines
        if len(self.prompt) > BIG_DISPLAY.get_width():
            self.aux_prompt = self.prompt[-BIG_DISPLAY.get_width():]
            BIG_DISPLAY.text(self.aux_prompt, 0, 20)

        BIG_DISPLAY.show()
            
    def execute(self, command):
        # Command to lowercase
        command = command.lower()
        # Split the command into parts
        parts = command.split()

        # Check if the command is empty
        if len(parts) == 0:
            return

        # Get the command name
        cmd = parts[0]
        # Get the command arguments
        args = parts[1:] if len(parts) > 1 else []

        # Check if the command exists
        if command_controller.is_command(cmd):
            # Execute the command
            if command_controller.execute_command(cmd, args) == "X":
                self.command_not_found(cmd)
        else:
            self.command_not_found(cmd)

    def command_not_found(self, cmd):
        BIG_DISPLAY.text("Command: " + cmd, 0, 25)
        BIG_DISPLAY.text("Not found", 0, 40)
        BIG_DISPLAY.show()
        time.sleep(2)
        # Clear the error message
        BIG_DISPLAY.clear()
        # Set the prompt to the user
        self.prompt = self.user
        self.display_prompt()
        input_buffer["errased"] = True