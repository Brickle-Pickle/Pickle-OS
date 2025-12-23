# Pickle OS

**The Crunchy Cyberdeck Terminal for Esp32 C3 SuperMini**

![MicroPython](https://img.shields.io/badge/MicroPython-Powered-blue?style=flat&logo=python)
![Hardware](https://img.shields.io/badge/ESP32-C3-red?style=flat&logo=Espressif)
![Status](https://img.shields.io/badge/Status-Alpha-orange)

**Pickle OS** is a shell environment and simulated operating system designed to run on the **Esp32 C3 SuperMini**. It transforms the microcontroller into a standalone "Cyberdeck" style mini-PC that operates independently of an external computer.

The system uses a **dual-screen architecture**: one display for terminal output and system feedback, and a secondary display dedicated exclusively to a dynamic virtual keyboard controlled by physical buttons.

## Key Features

* **Interactive Terminal:** Custom command-line interface (Shell) with history and visual feedback.
* **Real File System:** Functional commands to create, read, write, and delete files (`ls`, `cat`, `touch`, `rm`, `mkdir`).
* **Dedicated Virtual Keyboard:** Text input via a secondary OLED display and physical D-Pad navigation.
* **Storage:** SD Card support for file storage.
* **Retro UI:** Monochromatic pixel-art interface optimized for low-power displays.

## Hardware Requirements

This project is designed for the following BOM (Bill of Materials):

* **MCU:** Esp32 C3 SuperMini.
* **Displays:**
    * 1x OLED 128x128 (1.5" RGB/Mono) - *Main Monitor*.
    * 1x OLED 128x32 (0.91") - *Virtual Keyboard*.
* **Input:** 
    * 2x Push buttons (1 action + 1 back).
    * 1x D-Pad (4-directional + 1 action) - *Virtual Keyboard Navigation*.

## Pinout and Connections

Check the `system/config.py` file for detailed pin assignments and connections for displays, buttons, and other peripherals.

## Installation

1.  **Flash MicroPython:** Install the latest MicroPython UF2 firmware onto your Esp32 C3 SuperMini.
2.  **Dependencies:** Upload the `ssd1306.py` and `sdcard.py` library to the `lib/` folder on your device (available via Thonny package manager).
3.  **Deployment:**
    * Clone this repository.
    * Upload `main.py` (`app.py` if development still in progress), `boot.py`, and all other files to the root of the device (if you want to have the base folder structure and you are using a raspberry pi execute `mkfs.py` {JUST ONCE}).
4. **Erase the following files:**
    * `mkfs.py`
    * `README.md`
    * `home/user/README.md` (Optional if you know what you are doing) {You can update it with your own instructions}
5.  **Boot:** Reset the device or reconnect power.

## Available Commands

Once Pickle OS has booted, the following commands are available in the shell:

### Options
* `[]` - Mandatory argument.
* `{}` - Optional argument.
* `...` - Variable number of arguments.
* `or` - Alternate options.

### File System
* `ls {path} {-l} {-d or -f}` 
    - List files and directories (default path is current directory).
    - `path` - Path to the directory to list (relative or absolute), if empty it will list the current directory.
    - `-l` - List files with detailed information.
    - `-d` - List directories only.
    - `-f` - List files only.
* `cd {path}`
    - Change the current working directory.
    - `path` - Path to the directory to change to (relative or absolute), if empty it will change to the root directory.
    - `path = ..` - Go to the parent directory.
    - `path = /...` - Go to the ... directory starting from root (absolute path).
    - `path = ...` - Go to the ... directory starting from the current directory (relative path).
* `cat [file]`
    - Display the contents of a file (only works with `.txt` and `.py` files).
    - `file` - Path to the file to display (relative or absolute).
* `mkdir [dir_name]`
    - Create a new directory.
    - `dir_name` - Name of the directory to create.

### Utilities
* `help` - Show the help menu (commands and options).
* `reboot` - Restart the system.

## Roadmap

* [X] SD Card support (Mass storage).
* [ ] File system operations (create, show and delete files and directories).
* [X] Route navigation (absolute and relative paths).
* [ ] Full text editor (nano style extension `file.txt`).
* [ ] System monitor (CPU, memory, disk usage).
* [ ] User accounts and permissions.
* [ ] Benchmarking tools (CPU, memory, disk speed).
* [ ] Help menu (show available commands and options).
* [ ] Paint (simple pixel art editor extension `file.bitimg`).
* [ ] BitLense (simple image viewer extension `file.bitimg`).
* [ ] PassFinder (simple password manager extension `file.pass`) {`file.pass` [made with PassFinder] is a text file that contains the passwords in the format `name:password` you need to provide a password to access the file}.
* [ ] Crypter (convert `.txt` files to `.pass` files with a password).
* [ ] WiFi connectivity (HTTP Client / Local Chat).
* [ ] Mini-games (Snake / Pong).
* [ ] System settings (timezone, language, etc.).
* [ ] Mobile app for remote access.

## Contributing

Pull Requests are welcome! If you have ideas for optimizing the display driver or adding new "hacker-style" dummy commands, feel free to collaborate.

## License

This project is licensed under the MIT License - feel free to use it, modify it, and build your own Cyberdeck.
I would love to hear from you if you build something cool with this!