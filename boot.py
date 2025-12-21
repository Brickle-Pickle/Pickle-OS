# boot.py -> Its role is to set up the system environment before the main application starts.
from apps import splash
from system.config import SMALL_DISPLAY, SYSTEM_NAME, VERSION, BOARD_TYPE
import gc

# Enable garbage collection
gc.enable()

# Set up system configurations
print("[boot] System initialization started.")

gc.collect()
print("[boot] Free memory", gc.mem_free(), "bytes")
print("[boot] Boot complete.")

# Show some info on the small display
SMALL_DISPLAY.clear()
SMALL_DISPLAY.set_text_size(1)
SMALL_DISPLAY.text(SYSTEM_NAME, 0, 0)
SMALL_DISPLAY.text("----------", 0, 10)
SMALL_DISPLAY.text("Ver:" + VERSION, 0, 20)
SMALL_DISPLAY.show()

# Show splash animation
splash.show_splash()

# Clear display after splash
SMALL_DISPLAY.clear()