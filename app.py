# app.py -> Primary application logic.

import os
import sys
import gc
import time

print("[main] Application starting...")
# Sleep time for pc connection
time.sleep(3)

# Check file system status
print("[main] Checking file system status...")
print(os.listdir())

# Check folder structure
required_folders = ['system', 'bin', 'data', 'apps', 'home']

for folder in required_folders:
    try:
        os.stat(folder)
        print(f"[main] Folder exists: {folder}")
    except OSError:
        print(f"[main] Creating missing folder: {folder}")
        os.mkdir(folder)

'''
# Check its own imports
actual_import = 'system'

try:
    import system
    print("[main] 'system' module imported successfully.")

    actual_import = 'bin'
    import bin
    print("[main] 'bin' module imported successfully.")

    actual_import = 'data'
    import data
    print("[main] 'data' module imported successfully.")

    actual_import = 'apps'
    import apps
    print("[main] 'apps' module imported successfully.")

    actual_import = 'home'
    import home
    print("[main] 'home' module imported successfully.")
except ImportError:
    print("[main] Error:", actual_import, "module not found.")
'''

# Check memory status
gc.collect()
print("\n[main] Free memory", gc.mem_free(), "bytes")

# Todo: Start main application loop
'''
while True:
    print("[main] Main application loop running...")
'''