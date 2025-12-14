from machine import Pin, SoftI2C, I2C
from lib import ssd1306
from system import config
import time

print("Initializing displays...")

# Initialize first display (bigger)
try:
    i2c_big = SoftI2C(sda=Pin(config.SCREEN_BIG_SDA_PIN), scl=Pin(config.SCREEN_BIG_SCL_PIN), freq=400000)
    display_big = ssd1306.SSD1306_I2C(128, 64, i2c_big)
    display_big.fill(0)
    display_big.text("DISPLAY 1", 10, 20)
    display_big.show()
    print("Display 1 (I2C1) detected.")
except Exception as e:
    print(f"Error on Display 1: {e}")
    display_big = None

# Initialize second display (smaller)
try:
    i2c_small = I2C(0, sda=Pin(config.SCREEN_SMALL_SDA_PIN), scl=Pin(config.SCREEN_SMALL_SCL_PIN), freq=400000)
    display_small = ssd1306.SSD1306_I2C(128, 32, i2c_small)
    print("Display 2 (I2C0) detected.")
except Exception as e:
    print(f"Error on Display 2: {e}")
    display_small = None

# Main loop to update displays
while True:
    # Update first display
    if display_big:
        display_big.fill(0)
        display_big.text("DISP 1: 128x64", 0, 0)
        display_big.text("SSD1306 OK", 0, 10)
        display_big.text(f"T: {time.ticks_ms()/1000}", 0, 25)
        display_big.show()

    # Update second display
    if display_small:
        display_small.fill(0)
        display_small.text("DISPLAY 2 - OK", 0, 0)
        display_small.text("GP4/GP5 - I2C0", 0, 10)
        display_small.text(f"T: {time.ticks_ms()/1000}", 0, 20)
        display_small.show()
    
    time.sleep(0.1)
