# sd_reader.py -> Module to handle micro SD card operations.
import machine

class SDReader:
    def __init__(self, miso_pin, mosi_pin, clk_pin, cs_pin):
        self.spi = machine.SPI(1,
                               baudrate=1000000,
                               polarity=0,
                               phase=0,
                               sck=machine.Pin(clk_pin),
                               mosi=machine.Pin(mosi_pin),
                               miso=machine.Pin(miso_pin))
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)
        self.cs.value(1)  # Deselect the SD card

    def mount(self, mount_point="/sd"):
        import os
        from lib import sdcard
        self.sd = sdcard.SDCard(self.spi, self.cs)
        os.mount(self.sd, mount_point)

    def unmount(self, mount_point="/sd"):
        import os
        os.umount(mount_point)