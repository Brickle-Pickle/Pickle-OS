# crypter.py -> Encrypt txt files to pass files
import uos
import time
from system.config import BIG_DISPLAY, SMALL_DISPLAY, JOYSTICK
from system.keyboard import Keyboard
from system.shared_states import input_buffer

KEYBOARD = Keyboard()

def get_password():
    password = ""
    input_buffer["input"] = ""
    input_buffer["enter"] = False
    input_buffer["update_shell"] = False
    
    SMALL_DISPLAY.clear()
    SMALL_DISPLAY.text("Enter Password", 0, 0)
    SMALL_DISPLAY.text("JoyBtn to Confirm", 0, 10)
    SMALL_DISPLAY.show()
    
    BIG_DISPLAY.clear()
    BIG_DISPLAY.text("Password:", 0, 0)
    BIG_DISPLAY.show()
    
    while True:
        if JOYSTICK.is_button_pressed():
            time.sleep(0.5)
            return password
            
        input_buffer["input"] = " " 
        
        if KEYBOARD.read_input():
            time.sleep(0.2)
            
        if input_buffer["update_shell"]:
             if input_buffer["errased"]:
                 if len(password) > 0:
                     password = password[:-1]
             else:
                 char = input_buffer["input"][1:]
                 if char and char != "<" and char != ">":
                     password += char
            
             BIG_DISPLAY.clear()
             BIG_DISPLAY.text("Password:", 0, 0)
             BIG_DISPLAY.text("*" * len(password), 0, 10)
             BIG_DISPLAY.show()
             
             input_buffer["update_shell"] = False
             input_buffer["errased"] = False
             
        if KEYBOARD.needs_render:
            KEYBOARD.display_keyboard()

def crypter(args):
    if len(args) != 1:
        BIG_DISPLAY.show_info(["Usage:", "crypter <file>"])
        return

    file_name = args[0]
    if not file_name.endswith(".txt"):
        file_name += ".txt"
        
    file_path = input_buffer["actual_path"] + "/" + file_name
    
    try:
        uos.stat(file_path)
    except OSError:
        BIG_DISPLAY.show_info(["File not found"])
        return

    with open(file_path, "r") as f:
        content = f.read()
        
    password = get_password()
    
    if not password:
        BIG_DISPLAY.show_info(["No password set"])
        return

    encrypted = ""
    key_len = len(password)
    for i in range(len(content)):
        char_code = ord(content[i])
        key_code = ord(password[i % key_len])
        encrypted += chr(char_code ^ key_code)
        
    target_file = file_path.replace(".txt", ".pass")
        
    with open(target_file, "w") as f:
        f.write(encrypted)
        
    BIG_DISPLAY.show_info(["Encrypted saved"])

def help():
    BIG_DISPLAY.show_info(["Usage:", "crypter <file>"], 4)
