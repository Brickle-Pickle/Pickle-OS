# sdcard.py -> SD card driver for MicroPython using SPI interface.
import time

class SDCard:
    CMD_TIMEOUT = 100
    R1_IDLE_STATE = 1 << 0
    R1_ILLEGAL_COMMAND = 1 << 2
    TOKEN_CMD25 = 0xFC
    TOKEN_STOP_TRAN = 0xFD
    TOKEN_DATA = 0xFE

    def __init__(self, spi, cs, baudrate=1320000):
        import sys
        self.spi = spi
        self.cs = cs
        self.cmdbuf = bytearray(6)
        self.dummybuf = bytearray(512)
        self.tokenbuf = bytearray(1)
        for i in range(512):
            self.dummybuf[i] = 0xFF
        self.dummybuf_memoryview = memoryview(self.dummybuf)
        print("[sdcard] CS high (deselect)")
        self.cs(1)
        print("[sdcard] Sending 16 dummy clocks")
        for _ in range(16):
            self.spi.write(b"\xff")
        print("[sdcard] CS low (select)")
        self.cs(0)
        print("[sdcard] CMD0: GO_IDLE_STATE")
        for _ in range(self.CMD_TIMEOUT):
            if self.cmd(0, 0, 0x95) == self.R1_IDLE_STATE:
                print("[sdcard] Card is in IDLE state")
                break
        else:
            print("[sdcard] No SD card detected")
            raise OSError("no SD card")
        print("[sdcard] CMD8: SEND_IF_COND")
        r = self.cmd(8, 0x01AA, 0x87, 4)
        print("[sdcard] CMD8 response:", r)
        if r == self.R1_IDLE_STATE:
            print("[sdcard] Card is v2.0+")
            self.init_card_v2()
        elif r == (self.R1_IDLE_STATE | self.R1_ILLEGAL_COMMAND):
            print("[sdcard] Card is v1.x")
            self.init_card_v1()
        else:
            print("[sdcard] CMD8 response unexpected, trying to force v1.x...")
            try:
                self.init_card_v1()
            except Exception as e:
                print("[sdcard] Forcing v1.x failed:", e)
                raise OSError("couldn't determine SD card version")
        print("[sdcard] CMD9: SEND_CSD")
        if self.cmd(9, 0, 0, 0, False) != 0:
            print("[sdcard] No response from SD card (CMD9)")
            raise OSError("no response from SD card")
        csd = bytearray(16)
        self.readinto(csd)
        print("[sdcard] CSD register:", [hex(b) for b in csd])
        if csd[0] & 0xC0 == 0x40:
            self.sectors = ((csd[8] << 8 | csd[9]) + 1) * 1024
            print("[sdcard] SDHC/SDXC detected, sectors:", self.sectors)
        elif csd[0] & 0xC0 == 0x00:
            c_size = (csd[6] & 0b11) << 10 | csd[7] << 2 | csd[8] >> 6
            c_size_mult = (csd[9] & 0b11) << 1 | csd[10] >> 7
            read_bl_len = csd[5] & 0b1111
            capacity = (c_size + 1) * (2 ** (c_size_mult + 2)) * (2 ** read_bl_len)
            self.sectors = capacity // 512
            print("[sdcard] SDSC detected, sectors:", self.sectors)
        else:
            print("[sdcard] CSD format not supported")
            raise OSError("SD card CSD format not supported")
        if self.cmd(16, 512, 0) != 0:
            print("[sdcard] Could not set 512 block size")
            raise OSError("can't set 512 block size")
        print("[sdcard] Initialization complete, setting SPI baudrate")
        self.spi.init(baudrate=baudrate)

    def init_card_v1(self):
        for _ in range(self.CMD_TIMEOUT):
            if self.cmd(55, 0, 0) == self.R1_IDLE_STATE and self.cmd(41, 0, 0) == 0:
                self.cdv = 512
                return
        raise OSError("timeout waiting for v1 card")

    def init_card_v2(self):
        for _ in range(self.CMD_TIMEOUT):
            time.sleep_ms(50)
            if self.cmd(55, 0, 0) == self.R1_IDLE_STATE and self.cmd(41, 0x40000000, 0) == 0:
                if self.cmd(58, 0, 0, 4) & 0x40:
                    self.cdv = 1
                else:
                    self.cdv = 512
                return
        raise OSError("timeout waiting for v2 card")

    def cmd(self, cmd, arg, crc, final=0, release=True, skip1=False):
        self.cs(0)
        self.spi.write(b"\xff")
        buf = self.cmdbuf
        buf[0] = 0x40 | cmd
        buf[1] = arg >> 24
        buf[2] = arg >> 16
        buf[3] = arg >> 8
        buf[4] = arg
        buf[5] = crc
        self.spi.write(buf)
        if skip1:
            self.spi.readinto(self.tokenbuf, 0xFF)
        for _ in range(self.CMD_TIMEOUT):
            self.spi.readinto(self.tokenbuf, 0xFF)
            if not (self.tokenbuf[0] & 0x80):
                if final:
                    data = self.tokenbuf[0]
                    for _ in range(final):
                        self.spi.readinto(self.tokenbuf, 0xFF)
                        data = data << 8 | self.tokenbuf[0]
                    return data
                if release:
                    self.cs(1)
                    self.spi.write(b"\xff")
                return self.tokenbuf[0]
        self.cs(1)
        self.spi.write(b"\xff")
        return -1

    def readinto(self, buf):
        self.cs(0)
        while True:
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] == self.TOKEN_DATA:
                break
        mv = self.dummybuf_memoryview
        if len(buf) != len(mv):
            mv = mv[: len(buf)]
        self.spi.write_readinto(mv, buf)
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")
        self.cs(1)
        self.spi.write(b"\xff")

    def write(self, token, buf):
        self.cs(0)
        self.spi.read(1, token)
        self.spi.write(buf)
        self.spi.write(b"\xff")
        self.spi.write(b"\xff")
        while True:
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] != 0xFF:
                break
        if (self.tokenbuf[0] & 0x1F) != 0x05:
            self.cs(1)
            self.spi.write(b"\xff")
            return
        while True:
            self.spi.readinto(self.tokenbuf, 0xFF)
            if self.tokenbuf[0] == 0xFF:
                break
        self.cs(1)
        self.spi.write(b"\xff")

    def readblocks(self, block_num, buf):
        nblocks = len(buf) // 512
        assert nblocks and not len(buf) % 512, "Buffer length is invalid"
        if nblocks == 1:
            if self.cmd(17, block_num * self.cdv, 0, release=False) != 0:
                self.cs(1)
                raise OSError(5)
            self.readinto(buf)
        else:
            if self.cmd(18, block_num * self.cdv, 0, release=False) != 0:
                self.cs(1)
                raise OSError(5)
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.readinto(mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            if self.cmd(12, 0, 0xFF, skip1=True):
                raise OSError(5)

    def writeblocks(self, block_num, buf):
        nblocks, err = divmod(len(buf), 512)
        assert nblocks and not err, "Buffer length is invalid"
        if nblocks == 1:
            if self.cmd(24, block_num * self.cdv, 0) != 0:
                raise OSError(5)
            self.write(self.TOKEN_DATA, buf)
        else:
            if self.cmd(25, block_num * self.cdv, 0) != 0:
                raise OSError(5)
            offset = 0
            mv = memoryview(buf)
            while nblocks:
                self.write(self.TOKEN_CMD25, mv[offset : offset + 512])
                offset += 512
                nblocks -= 1
            self.write(self.TOKEN_STOP_TRAN, b"")

    def ioctl(self, op, arg):
        if op == 4:
            return self.sectors
        if op == 5:
            return 512