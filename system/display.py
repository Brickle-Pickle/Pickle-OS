# display.py -> Manages display initialization and rendering.
from machine import Pin, SoftI2C
import framebuf
import time
from lib import ssd1306
from system.shared_states import input_buffer

class Display:
    def __init__(self, width, height, scl_pin, sda_pin, i2c_id, i2c_addr):
        self.i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c)
        self.text_size = 1

    def fill(self, color):
        self.display.fill(color)
        self.display.show()

    def fill_rect(self, x, y, w, h, c):
        self.display.fill_rect(x, y, w, h, c)

    def pixel(self, x, y, c):
        self.display.pixel(x, y, c)

    def hline(self, x, y, w, c):
        self.display.hline(x, y, w, c)

    def vline(self, x, y, h, c):
        self.display.vline(x, y, h, c)

    def text(self, string, x, y, color=1):
        if self.text_size == 1:
            if color == "inverted":
                # Fill the background of the actual text position
                self.display.fill_rect(x, y, len(string) * 8, 8, 1)
                # Draw the text on top of the filled background
                self.display.text(string, x, y, 0)
            else:
                self.display.text(string, x, y, color)
        else:
            self._draw_scaled_text(string, x, y, color, self.text_size)

    def _draw_scaled_text(self, string, x, y, color, size):
        if color == "inverted":
            # Pre-calculate the bounding box for the entire string
            total_width = len(string) * (size * 4)  # Approximate width
            total_height = size * 4  # Approximate height
            self.display.fill_rect(x, y, total_width, total_height, 1)
            draw_color = 0
        else:
            draw_color = color

        sizes = {1: 6, 2: 8, 3: 10, 4: 12}
        target_size = sizes.get(size, 8)
        src_size = 8
        temp_buf = bytearray(src_size * src_size // 8)
        temp_fb = framebuf.FrameBuffer(temp_buf, src_size, src_size, framebuf.MONO_VLSB)
        for i, char in enumerate(string):
            temp_fb.fill(0)
            temp_fb.text(char, 0, 0, 1)
            for py in range(target_size):
                for px in range(target_size):
                    src_x = px * src_size // target_size
                    src_y = py * src_size // target_size
                    if temp_fb.pixel(src_x, src_y):
                        draw_x = x + (i * target_size) + px
                        draw_y = y + py
                        if 0 <= draw_x < self.display.width and 0 <= draw_y < self.display.height:
                            self.display.pixel(draw_x, draw_y, draw_color)

    def show(self):
        self.display.show()
    
    def clear(self):
        self.fill(0)
        self.show()
    
    def get_width(self):
        return self.display.width
    def get_height(self):
        return self.display.height
    
    def load_bitmap(self, bitmap):
        self.display.buffer[:] = bitmap

    def set_text_size(self, size):
        self.text_size = max(1, min(size, 4))
    
    def show_info(self, error_messages, duration=2):
        self.clear()
        for i, msg in enumerate(error_messages):
            self.text(msg, 0, i * 10)
        self.show()
        time.sleep(duration)
        # Clear the error message
        self.clear()
        # Reset shell state
        input_buffer["input"] = " "
        input_buffer["update_shell"] = False
        input_buffer["errased"] = True
        input_buffer["enter"] = False
        input_buffer["reset_shell"] = True