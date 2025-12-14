# config.py -> Its role is to manage system-wide configurations and settings.
from system.leds import LEDController
from system.buzzer import BuzzerController

# Constant definitions
SYSTEM_NAME = "PickleOS"
VERSION = "0.0.3"
DEBUG_MODE = True

# Pin configurations
LED_RED_PIN = 7
LED_GREEN_PIN = 6
SCREEN_BIG_SDA_PIN = 3
SCREEN_BIG_SCL_PIN = 2
SCREEN_SMALL_SDA_PIN = 4
SCREEN_SMALL_SCL_PIN = 5
BUZZER_PIN = 22

# LEDs
RED_LED = LEDController(LED_RED_PIN)
GREEN_LED = LEDController(LED_GREEN_PIN)

# Buzzer settings
BUZZER_FREQUENCY_STANDARD = 2000  # in Hz
BUZZER_FREQUENCY_HIGH = 3000      # in Hz  
BUZZER_DURATION_SHORTER = 0.1
BUZZER_DURATION_SHORT = 0.2
BUZZER_DURATION_MID = 0.5
BUZZER_DURATION_LONG = 0.7
BUZZER_DURATION_LONGER = 1.0
BUZZER = BuzzerController(BUZZER_PIN)