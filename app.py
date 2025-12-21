# app.py -> Primary application logic.

import os
import gc
import time

print("[main] Application starting...")
# Sleep time for pc connection
time.sleep(3)

# Check file system status
print("[main] Checking file system status...")
print(os.listdir())

# Check memory status
gc.collect()
print("\n[main] Free memory", gc.mem_free(), "bytes")

# Test controllers
from system.config import BUTTON_LEFT, BUTTON_RIGHT, JOYSTICK
print("\n[main] Testing Buttons and Joystick...")
print(" Press LEFT button...")
while not BUTTON_LEFT.is_pressed():
    pass
print(" LEFT button pressed.")

print(" Press RIGHT button...")
while not BUTTON_RIGHT.is_pressed():
    pass
print(" RIGHT button pressed.")

print(" Move Joystick and press its button...")
while not JOYSTICK.is_button_pressed():
    print(" Joystick position:", JOYSTICK.get_position())
    time.sleep(0.5)
    pass
print(" Joystick button pressed.")

# Test displays
from system.config import BIG_DISPLAY, SMALL_DISPLAY

print("\n[main] Testing Displays...")
BIG_DISPLAY.fill(0)
SMALL_DISPLAY.fill(0)
time.sleep(2)

BIG_DISPLAY.fill(1)
BIG_DISPLAY.show()
SMALL_DISPLAY.fill(1)
SMALL_DISPLAY.show()
time.sleep(3)

BIG_DISPLAY.clear()
SMALL_DISPLAY.clear()

# Test micro SD card reader
from system.config import init_sd_reader
print("\n[main] Testing Micro SD Card Reader...")
try:
    SD_READER = init_sd_reader()
    SD_READER.mount()
    print(" Micro SD card mounted successfully.")
    print(" Contents:", os.listdir("/sd"))
    SD_READER.unmount()
    print(" Micro SD card unmounted successfully.")
except Exception as e:
    print(" Micro SD card test failed:", e)

print("\n[main] All tests completed. Application is running.")