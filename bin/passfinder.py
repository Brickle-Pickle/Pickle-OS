# passfinder.py -> View encrypted pass files
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

def passfinder(args):
    if len(args) != 1:
        BIG_DISPLAY.show_info(["Usage:", "passfinder <file>"])
        return

    file_name = args[0]
    
    # If user didn't provide extension, try adding .pass
    if not file_name.endswith(".pass"):
        if not "." in file_name:
             file_name += ".pass"
        
    file_path = input_buffer["actual_path"] + "/" + file_name
    
    try:
        uos.stat(file_path)
    except OSError:
        BIG_DISPLAY.show_info(["File not found"])
        return
        
    with open(file_path, "r") as f:
        encrypted = f.read()
        
    password = get_password()
    
    if not password:
         BIG_DISPLAY.show_info(["Password required"])
         return
         
    decrypted = ""
    key_len = len(password)
    for i in range(len(encrypted)):
        char_code = ord(encrypted[i])
        key_code = ord(password[i % key_len])
        decrypted += chr(char_code ^ key_code)
        
    lines = decrypted.split('\n')
    
    SMALL_DISPLAY.clear()
    SMALL_DISPLAY.text("Exit: Joy Button", 0, 0)
    SMALL_DISPLAY.text("Scroll: Joystick", 0, 10)
    SMALL_DISPLAY.show()
    
    scroll_offset = 0
    max_lines = 8
    
    while True:
        BIG_DISPLAY.clear()
        for i in range(max_lines):
            idx = scroll_offset + i
            if idx < len(lines):
                BIG_DISPLAY.text(lines[idx][:21], 0, i * 8)
        BIG_DISPLAY.show()
        
        x, y = JOYSTICK.get_position()
        
        # Scroll down
        if y > 60000:
            if scroll_offset + max_lines < len(lines):
                scroll_offset += 1
            time.sleep(0.1)
            
        # Scroll up
        elif y < 1000:
            if scroll_offset > 0:
                scroll_offset -= 1
            time.sleep(0.1)
            
        if JOYSTICK.is_button_pressed():
            # Reset UI state
            input_buffer["reset_shell"] = True
            input_buffer["reset_keyboard"] = True
            time.sleep(0.5)
            break
            
        time.sleep(0.05)

def help():
    BIG_DISPLAY.show_info(["Usage:", "passfinder <file>"], 4)
