# Pickle OS

**The Crunchy Cyberdeck Terminal for RP2040**

![MicroPython](https://img.shields.io/badge/MicroPython-Powered-blue?style=flat&logo=python)
![Hardware](https://img.shields.io/badge/Hardware-RP2040-red?style=flat&logo=raspberrypi)
![Status](https://img.shields.io/badge/Status-Alpha-orange)

**Pickle OS** is a shell environment and simulated operating system designed to run on the **Esp32 C3 SuperMini**. It transforms the microcontroller into a standalone "Cyberdeck" style mini-PC that operates independently of an external computer.

The system uses a **dual-screen architecture**: one display for terminal output and system feedback, and a secondary display dedicated exclusively to a dynamic virtual keyboard controlled by physical buttons.

## Key Features

* **Interactive Terminal:** Custom command-line interface (Shell) with history and visual feedback.
* **Real File System:** Functional commands to create, read, write, and delete files (`ls`, `cat`, `touch`, `rm`, `mkdir`).
* **Dedicated Virtual Keyboard:** Text input via a secondary OLED display and physical D-Pad navigation.
* **Hardware Control:** Native commands to read sensors (temperature) and control actuators (LEDs, Buzzer).
* **Retro UI:** Monochromatic pixel-art interface optimized for low-power displays.

## Hardware Requirements

This project is designed for the following BOM (Bill of Materials):

* **MCU:** Esp32 C3 SuperMini.
* **Displays:**
    * 1x OLED 128x128 (1.5" RGB/Mono) - *Main Monitor*.
    * 1x OLED 128x32 (0.91") - *Virtual Keyboard*.
* **Input:** 5x Push buttons (4 for direction + 1 action/back).

## Pinout and Connections

Check the `system/config.py` file for detailed pin assignments and connections for displays, buttons, and other peripherals.

## Installation

1.  **Flash MicroPython:** Install the latest MicroPython UF2 firmware onto your Esp32 C3 SuperMini.
2.  **Dependencies:** Upload the `ssd1306.py` and `sdcard.py` library to the `lib/` folder on your device (available via Thonny package manager).
3.  **Deployment:**
    * Clone this repository.
    * Upload `main.py`, `boot.py`, and all other files to the root of the device (if you want to have the base folder structure in pico execute `mkfs.py` {JUST ONCE}).
4.  **Boot:** Reset the device or reconnect power.

## Available Commands

Once Pickle OS has booted, the following commands are available in the shell:

### File System
* `ls` - List files and directories.
* `cat [file]` - Display file content.
* `touch [file]` - Create an empty file.
* `rm [file]` - Delete a file.
* `mkdir [dir]` - Create a directory.
* `cd [path]` - Change directory.

### Hardware & Utilities
* `temp` - Show internal CPU temperature.
* `clear` - Clear the main screen.
* `reboot` - Restart the system.

## Roadmap

* [X] SD Card support (Mass storage).
* [ ] Full text editor (nano style).
* [ ] WiFi connectivity (HTTP Client / Local Chat).
* [ ] Mini-games (Snake / Pong).

## Contributing

Pull Requests are welcome! If you have ideas for optimizing the display driver or adding new "hacker-style" dummy commands, feel free to collaborate.

## License

This project is licensed under the MIT License - feel free to use it, modify it, and build your own Cyberdeck.