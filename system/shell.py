# shell.py -> Shell interface for the MiniPC.
import uos
from bin import cat, cd, ls, mkdir, rm
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY

class Shell:
    def __init__(self, user):
        self.prompt = user + "> "
        self.commands = {
            "cat": cat,
            "cd": cd,
            "ls": ls,
            "mkdir": mkdir,
            "rm": rm,
        }
        self.current_dir = "/"
        self.running = True
        self.history = []
        self.history_index = 0
        self.history_max = 10

    def display_prompt(self):
        BIG_DISPLAY.text(self.prompt, 0, 10)

        # Verify if the prompt is too long to fit in the display and print it in separate lines
        if len(self.prompt) > BIG_DISPLAY.get_width():
            self.aux_prompt = self.prompt[-BIG_DISPLAY.get_width():]
            BIG_DISPLAY.text(self.aux_prompt, 0, 20)

        BIG_DISPLAY.show()

    def run(self):
        print("Shell is running...")
        while self.running:
            # Get the command from the input buffer
            self.display_prompt()
            self.prompt = self.prompt + input_buffer["input"]

            # Execute the command if the enter key is pressed
            if input_buffer["enter"]:
                input_buffer["enter"] = False
                command = input_buffer["input"]
                input_buffer["input"] = ""
                self.history.append(command)
                self.history_index = len(self.history)
                if self.history_index > self.history_max:
                    self.history_index = self.history_max
                if command == "exit":
                    self.running = False
                    # Exit the shell, print bye and shutdown the MiniPC
                    BIG_DISPLAY.text("bye", 0, 30)

                    # Shutdown the MiniPC
                    uos.umount("/")
                    uos.sync()
                    uos.exit()
                else:
                    self.execute(command)
            
    def execute(self, command):
        # Split the command into parts
        parts = command.split()

        # Check if the command is empty
        if len(parts) == 0:
            return

        # Get the command name
        cmd = parts[0]
        # Get the command arguments
        args = parts[1:]

        # Check if the command exists
        if cmd in self.commands:
            # Execute the command
            self.commands[cmd](*args)
        else:
            # Print an error message
            BIG_DISPLAY.text("Command not found", 0, 30)
            time.sleep(2)
            # Clear the error message
            BIG_DISPLAY.clear()