# boot.py -> Its role is to set up the system environment before the main application starts.
from apps import splash
import gc

# Enable garbage collection
gc.enable()

# Set up system configurations
print("[boot] System initialization started.")

gc.collect()
print("[boot] Free memory", gc.mem_free(), "bytes")
print("[boot] Boot complete.")

# Show splash animation
splash.show_splash()

# Transition to main application
#import app