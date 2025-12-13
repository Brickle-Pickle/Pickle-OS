# Pickle OS

**The Crunchy Cyberdeck Terminal for RP2040**

![MicroPython](https://img.shields.io/badge/MicroPython-Powered-blue?style=flat&logo=python)
![Hardware](https://img.shields.io/badge/Hardware-RP2040-red?style=flat&logo=raspberrypi)
![Status](https://img.shields.io/badge/Status-Alpha-orange)

**Pickle OS** is a shell environment and simulated operating system designed to run on the **Raspberry Pi Pico (RP2040)**. It transforms the microcontroller into a standalone "Cyberdeck" style mini-PC that operates independently of an external computer.

The system uses a **dual-screen architecture**: one display for terminal output and system feedback, and a secondary display dedicated exclusively to a dynamic virtual keyboard controlled by physical buttons.

## Key Features

* **Interactive Terminal:** Custom command-line interface (Shell) with history and visual feedback.
* **Real File System:** Functional commands to create, read, write, and delete files (`ls`, `cat`, `touch`, `rm`, `mkdir`).
* **Dedicated Virtual Keyboard:** Text input via a secondary OLED display and physical D-Pad navigation.
* **Hardware Control:** Native commands to read sensors (temperature) and control actuators (LEDs, Buzzer).
* **Retro UI:** Monochromatic pixel-art interface optimized for low-power displays.

## Hardware Requirements

This project is designed for the following BOM (Bill of Materials):

* **MCU:** Raspberry Pi Pico W (or standard Pico).
* **Displays:**
    * 1x OLED 128x128 (1.5" RGB/Mono) - *Main Monitor*.
    * 1x OLED 128x32 (0.91") - *Virtual Keyboard*.
* **Input:** 5x Push buttons (4 for direction + 1 action/back).
* **Sensors:**
    * Temperature sensor (Integrated in RP2040).
* **Extras:**
    * 1x Buzzer (Passive/Active).
    * 2x LEDs (Red, Green).
    * Resistors and decoupling capacitors.

## Pinout and Connections

Pickle OS uses two independent I2C buses to maximize display refresh rates and avoid addressing conflicts.

| Component | Physical Pin | Function | Notes |
| :--- | :--- | :--- | :--- |
| **OLED Main (128x128)** | GP2 | SCL (I2C1) | Main Monitor |
| | GP3 | SDA (I2C1) | |
| **OLED Keyb (128x32)** | GP5 | SCL (I2C0) | Virtual Keyboard |
| | GP4 | SDA (I2C0) | |
| **Buttons** | GP17 | UP | Internal Pull-up |
| | GP18 | DOWN | Internal Pull-up |
| | GP19 | LEFT | Internal Pull-up |
| | GP20 | RIGHT | Internal Pull-up |
| | GP21 | BACK/ENTER | Internal Pull-up |
| **Sensors/Actuators** | GP13 | Buzzer | PWM |
| | GP14 | Green LED | |
| | GP15 | Red LED | |
| | GP12 | TRIG/SDA | HC-SR04 or VL53L0X |
| | GP11 | ECHO/SCL | *Check voltage levels* |

> **Note:** If using the HC-SR04 sensor, ensure you use a voltage divider on the ECHO pin to step down the 5V signal to 3.3V to protect the Pico GPIO.

## Installation

1.  **Flash MicroPython:** Install the latest MicroPython UF2 firmware onto your Raspberry Pi Pico.
2.  **Dependencies:** Upload the `ssd1306.py` library to the `lib/` folder on your Pico (available via Thonny package manager).
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
* `beep [hz] [ms]` - Play a tone via the buzzer.
* `led [color] [on/off]` - Control status LEDs.
* `clear` - Clear the main screen.
* `reboot` - Restart the system.

## Roadmap

* [ ] SD Card support (Mass storage).
* [ ] Full text editor (nano style).
* [ ] WiFi connectivity (HTTP Client / Local Chat).
* [ ] Mini-games (Snake / Pong).

## Contributing

Pull Requests are welcome! If you have ideas for optimizing the display driver or adding new "hacker-style" dummy commands, feel free to collaborate.

## License

This project is licensed under the MIT License - feel free to use it, modify it, and build your own Cyberdeck.