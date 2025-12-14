# leds.py -> Its role is to manage the LED indicators on the device.
import machine
import time

class LEDController:
    def __init__(self, pin_number):
        self.led = machine.Pin(pin_number, machine.Pin.OUT)
        self.actual_state = 0
        self.led.value(0)

    def on(self):
        self.led.value(1)
        self.actual_state = 1
        

    def off(self):
        self.led.value(0)
        self.actual_state = 0

    def blink(self, duration=0.5, times=3):
        for _ in range(times):
            self.on()
            time.sleep(duration)
            self.off()
            time.sleep(duration)