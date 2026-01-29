# config.py -> Its role is to manage system-wide configurations and settings.
from system.input import Button, Joystick
from system.display import Display
from system.sd_reader import SDReader

# Constant definitions
SYSTEM_NAME = "PickleOS"
DEVELOPER = "BRICKLE PICKLE"
VERSION = "0.5.2"
DEBUG_MODE = False
BOARD_TYPE = "ESP32-C3"  # Options: "PICO", "ESP32-C3"

# Pin configurations for ESP32-C3 Super Mini
# Available GPIO: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 21
# ADC pins: 0, 1, 2, 3, 4 (ADC1 channels)
# Both displays share the same I2C bus (different addresses: 0x3C and 0x3D)
# Make sure to change the address jumper on one display PCB
SMALL_SCREEN_SDA_PIN = 8
SMALL_SCREEN_SCL_PIN = 9
BIG_SCREEN_SDA_PIN = 10
BIG_SCREEN_SCL_PIN = 3

BUTTON_LEFT_PIN = 21
BUTTON_RIGHT_PIN = 20

JOYSTICK_X_PIN = 0   # ADC1_CH0 - Must use GPIO0-4 for analog input on ESP32-C3
JOYSTICK_Y_PIN = 1   # ADC1_CH1
JOYSTICK_BUTTON_PIN = 2

MICRO_SD_MISO_PIN = 4
MICRO_SD_MOSI_PIN = 5
MICRO_SD_CLK_PIN = 6
MICRO_SD_CS_PIN = 7

# Displays
BIG_DISPLAY = Display(128, 64, BIG_SCREEN_SCL_PIN, BIG_SCREEN_SDA_PIN, i2c_id=0, i2c_addr=0x3C)
SMALL_DISPLAY = Display(128, 32, SMALL_SCREEN_SCL_PIN, SMALL_SCREEN_SDA_PIN, i2c_id=-1, i2c_addr=0x3C)

# Buttons
BUTTON_LEFT = Button(BUTTON_LEFT_PIN)
BUTTON_RIGHT = Button(BUTTON_RIGHT_PIN)

# Joystick
JOYSTICK = Joystick(JOYSTICK_X_PIN, JOYSTICK_Y_PIN, JOYSTICK_BUTTON_PIN)

# Micro SD Card Reader
SD_READER = None

def init_sd_reader():
    global SD_READER
    if SD_READER is None:
        SD_READER = SDReader(MICRO_SD_MISO_PIN, MICRO_SD_MOSI_PIN, MICRO_SD_CLK_PIN, MICRO_SD_CS_PIN)
    return SD_READER