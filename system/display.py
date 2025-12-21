# display.py -> Manages display initialization and rendering.
import machine
import framebuf
from lib import ssd1306

class Display:
    def __init__(self, width, height, scl_pin, sda_pin, i2c_addr):
        self.i2c = machine.I2C(0, scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=400000)
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c, addr=i2c_addr)
        self.text_size = 1

    def fill(self, color):
        self.display.fill(color)
        self.display.show()

    def text(self, string, x, y, color=1):
        if self.text_size == 1:
            self.display.text(string, x, y, color)
        else:
            self._draw_scaled_text(string, x, y, color, self.text_size)

    def _draw_scaled_text(self, string, x, y, color, size):
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
                            self.display.pixel(draw_x, draw_y, color)

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
        