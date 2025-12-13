# Filesystem creation script (mkfs.py, only the first time)
import os

folders = [
    "system",
    "apps",
    "bin",
    "home",
    "home/user",
    "data",
    "data/logs",
    "lib",
]

for f in folders:
    try:
        os.mkdir(f)
    except OSError:
        pass

print("Filesystem structure created.")