# input.py -> Its role is to manage user input devices like buttons and joystick.
import machine

class Button:
    def __init__(self, pin_number):
        self.button = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)

    def is_pressed(self):
        return self.button.value() == 0  # true if pressed

class Joystick:
    def __init__(self, x_pin_number, y_pin_number, button_pin_number):
        # ESP32-C3 ADC configuration
        # ADC on ESP32-C3 has 12-bit resolution (0-4095) by default
        # Use attenuation for full 0-3.3V range
        self.x_axis = machine.ADC(machine.Pin(x_pin_number))
        self.y_axis = machine.ADC(machine.Pin(y_pin_number))
        # Set attenuation for 0-3.3V range (11dB attenuation)
        try:
            self.x_axis.init(atten=machine.ADC.ATTN_11DB)  # type: ignore
            self.y_axis.init(atten=machine.ADC.ATTN_11DB)  # type: ignore
        except:
            pass  # Some MicroPython versions may not support this
        self.button = Button(button_pin_number)

    def get_position(self):
        # ESP32-C3 uses read() which returns 0-4095 (12-bit)
        # Convert to 16-bit range (0-65535) for compatibility
        try:
            x_value = self.x_axis.read_u16()
            y_value = self.y_axis.read_u16()
        except:
            # Fallback for ESP32-C3: read() returns 12-bit, scale to 16-bit
            x_value = self.x_axis.read() * 16
            y_value = self.y_axis.read() * 16
        return (x_value, y_value)

    def is_button_pressed(self):
        return self.button.is_pressed()