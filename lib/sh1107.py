from micropython import const
from framebuf import FrameBuffer, MONO_VLSB

class SH1107(FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False, rotate=0):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.rotate = rotate
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytes([0x00, cmd]))

    def show(self):
        for page in range(self.height // 8):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x00)
            self.write_cmd(0x10)
            # Adjust mapping based on rotation or specific module offset
            # Some 128x128 modules need an offset of 0, others differ.
            # Try varying the start index if image is shifted.
            self.i2c.writeto(self.addr, b'\x40' + self.buffer[self.width * page:self.width * (page + 1)])

    def init_display(self):
        self.write_cmd(0xAE) # Display OFF
        self.write_cmd(0xDC) # Set Display Start Line
        self.write_cmd(0x00)
        self.write_cmd(0x81) # Contrast control
        self.write_cmd(0x2F)
        self.write_cmd(0x20) # Memory addressing mode
        self.write_cmd(0xA0 | (0x01 if self.rotate == 180 else 0x00)) # Seg remap
        self.write_cmd(0xC0 | (0x08 if self.rotate == 180 else 0x00)) # Com scan dir
        self.write_cmd(0xA8) # Multiplex ratio
        self.write_cmd(self.height - 1)
        self.write_cmd(0xD3) # Display offset
        self.write_cmd(0x60) # Sometimes 0x00, sometimes 0x60 depending on the module
        self.write_cmd(0xD5) # Clock divide ratio
        self.write_cmd(0x51)
        self.write_cmd(0xD9) # Pre-charge period
        self.write_cmd(0x22)
        self.write_cmd(0xDB) # VCOMH Deselect
        self.write_cmd(0x35)
        self.write_cmd(0xB0) # Page addr
        self.write_cmd(0xA4) # Entire display on/off
        self.write_cmd(0xA6) # Normal/Inverse
        self.write_cmd(0xAF) # Display ON
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(0xAE)

    def poweron(self):
        self.write_cmd(0xAF)