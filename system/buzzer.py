# buzzer.py -> Its role is to manage the buzzer functionality on the device.
import machine
import time

class BuzzerController:
    def __init__(self, pin_number):
        self.buzzer_pwm = machine.PWM(machine.Pin(pin_number))
        self.buzzer_pwm.duty_u16(0)
        self.volume = 32768

    def on(self):
        self.buzzer_pwm.duty_u16(self.volume)

    def off(self):
        self.buzzer_pwm.duty_u16(0)

    def set_volume(self, level):
        if 0 <= level <= 100:
            self.volume = int((level / 100) * 65535)

    def beep(self, duration=0.1, frequency=2000):
        self.buzzer_pwm.freq(frequency)
        self.on()
        time.sleep(duration)
        self.off()

    def play_tone(self, frequency, duration):
        self.buzzer_pwm.freq(frequency)
        self.on()
        time.sleep(duration)
        self.off()

    def play_melody(self, melody):
        for note, duration in melody:
            self.play_tone(note, duration)
            time.sleep(0.05)