# wifi.py -> WiFi interface for the MiniPC. 

"""

@ IMPORTANT @

The keyboard only supports lowercase letters, no numbers or special characters.
This means that if your WiFi password contains uppercase letters, numbers, or special characters,
you will not be able to enter it correctly using the current keyboard implementation.

If your WiFi password contains any of these unsupported characters and you wanna use this wifi module,
this is what you can do:

1. Change your WiFi password to a simpler one that only contains lowercase letters and spaces. 
    (Not recommended for security reasons, but it's a quick fix.)
2. Modify the keyboard implementation in system/keyboard.py to include support for uppercase letters,
    numbers, and special characters. This would involve adding these characters to the keyboard map
    and ensuring the input handling logic can process them correctly.
    (This is the recommended approach if you want to keep your original password and have a more versatile keyboard.)
3. What I (Brickle Pickle) recommend and what I also did.
    in the file `system/wifi_manager.py`, in the function `connect_to_wifi`,
    is a call to a file called `env.py` that contains the SSID and PASSWORD of your wifi.
    You can create this file in the root directory of your MiniPC with the following content:
    ```python
        def wifi_password():
            return "your_actual_wifi_password"
        def wifi_ssid():
            return "your_actual_wifi_ssid"
    ```

@ END OF IMPORTANT @

"""

import uos
from system.config import BIG_DISPLAY, SMALL_DISPLAY, BUTTON_LEFT, JOYSTICK
from system.keyboard import Keyboard
from system.shared_states import input_buffer
from system.wifi_manager import connect_to_wifi, get_wifi_status, test_connection
from system.shared_states import input_buffer
import env
import time

def wifi(args):
    if len(args) < 1 or len(args) > 3:
        help(args)
        return

    # Check for status command
    if args[0] == "status":
        show_status()
        return
    
    # Check for test command
    if args[0] == "test":
        show_test()
        return

    # Check for send command
    if args[0] == "send" or args[0] == "-s":
        send_text_notification(args[1])
        return

    # Hardcoded wifi connection
    if args[0] == "fake":
        connect_to_wifi("fake", None)
        input_buffer["reset_shell"] = True
        return
    if args[0] == "mb":
        connect_to_wifi("mobile", None)
        input_buffer["reset_shell"] = True
        return

    ssid = args[0]
    password = None

    # Check for -p flag for password
    if len(args) == 3 and args[1] == "-p":
        password = args[2]
    else:
        password = ask_for_password()

    # Wifi connection logic
    connect_to_wifi(ssid, password)
    input_buffer["reset_shell"] = True

def ask_for_password():
    password = ""
    passwordChanged = False
    keyboard = Keyboard()

    while True:
        # Check for user input
        if (keyboard.read_input()):
            # If a key was pressed, wait a bit to avoid double presses
            if not input_buffer["enter"]:
                passwordChanged = True
                password = input_buffer["input"]

            time.sleep(0.2)

        if keyboard.needs_render:
            keyboard.display_keyboard()

        if input_buffer["enter"]:
            password = input_buffer["input"]
            input_buffer["enter"] = False
            input_buffer["input"] = ""
            return password

        if passwordChanged:
            BIG_DISPLAY.set_text_size(1)
            BIG_DISPLAY.text("Enter WiFi Password:", 0, 10)
            BIG_DISPLAY.text("Press enter when done", 0, 22)
            BIG_DISPLAY.text("Password: " + "*" * len(password), 0, 35)
            BIG_DISPLAY.show()
            passwordChanged = False

def show_status():
    status = get_wifi_status()
    
    if not status["connected"]:
        BIG_DISPLAY.show_info([status["message"]], 3)
        return
    
    info = [
        "WiFi Status:",
        "SSID: " + status["ssid"],
        "IP: " + status["ip"],
        "Gateway: " + status["gateway"]
    ]
    BIG_DISPLAY.show_info(info, 5)
    input_buffer["reset_shell"] = True

def show_test():
    BIG_DISPLAY.show_info(["Testing connection..."], 1)
    success, message = test_connection()
    
    if success:
        BIG_DISPLAY.show_info(["Connection test:", "SUCCESS!", message], 3)
    else:
        BIG_DISPLAY.show_info(["Connection test:", "FAILED!", message], 3)

def send_text_notification(message):
    """
        To send a text notification to a connected mobile device,
        you need to have the ntfy mobile app installed and configured
        on your phone.
    """
    
    import urequests
    url = "https://ntfy.sh/" + env.ntfy_topic()  # Get the ntfy URL from env.py

    try:   
        response = urequests.post(
            url, 
            data=message,
            headers={"Title": "MiniPC Notification", "Priority": "high"} # High priority
        )

        if response.status_code == 200:
            BIG_DISPLAY.show_info(["Notification sent!"], 2)
        else:
            BIG_DISPLAY.show_info(["Failed to send", "notification."], 2)
    
    except Exception as e:
        BIG_DISPLAY.show_info(["Error sending", "notification."], 2)

def help(args):
    SMALL_DISPLAY.set_text_size(1)
    SMALL_DISPLAY.show_info(["wifi [ssid] {-p [pass]}", "wifi status", "wifi test", "Connect or check WiFi"], 5)