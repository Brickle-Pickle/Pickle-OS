# shell.py -> Shell interface for the MiniPC.
import uos
import time
from bin import command_controller
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY

class Shell:
    def __init__(self, user):
        self.user = user
        self.current_dir = "/"
        self.running = True
        self.history = []
        self.history_index = 0
        self.history_max = 10
        self.prompt = self.user + input_buffer["actual_path"] + "> "
        self.display_prompt()

    def display_prompt(self):
        if input_buffer["errased"]:
            BIG_DISPLAY.clear()
            input_buffer["errased"] = False
        
        # We assume a character width of 8 pixels
        num_chars = BIG_DISPLAY.get_width() // 8
        
        if len(self.prompt) > num_chars:
            # Split the prompt into lines
            lines = [self.prompt[i:i+num_chars] for i in range(0, len(self.prompt), num_chars)]
            for i, line in enumerate(lines):
                BIG_DISPLAY.text(line, 0, 10 + i * 10)
        else:
            BIG_DISPLAY.text(self.prompt, 0, 10)

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
        BIG_DISPLAY.show_error(["Command: " + cmd, "Not found"])
