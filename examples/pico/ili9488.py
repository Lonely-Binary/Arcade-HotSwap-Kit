"""ILI9488 480x320 SPI driver; adapted from the kit bench tests."""
import time
from machine import Pin, SPI

def _rgb565_to_rgb666(color):
    r5 = (color >> 11) & 0x1F
    g6 = (color >> 5) & 0x3F
    b5 = color & 0x1F
    return bytes((b5 << 3, g6 << 2, r5 << 3))

class ILI9488:
    WIDTH = 480
    HEIGHT = 320

    def __init__(self, spi, cs, dc, rst, bl=None):

        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.bl = bl

    def _hw_reset(self):
        if self.rst is None:
            return
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(20)
        self.rst(1)
        time.sleep_ms(120)

    def _write_cmd(self, c):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes((c,)))
        self.cs(1)

    def _write_data(self, buf):
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)

    def init(self):
        if self.bl is not None:
            self.bl.init(Pin.OUT)
            self.bl(1)

        self.cs.init(Pin.OUT)
        self.cs(1)
        self.dc.init(Pin.OUT)
        self.dc(0)
        if self.rst is not None:
            self.rst.init(Pin.OUT)

        self._hw_reset()

        gamma_p = bytes(
            (
                0x00,
                0x03,
                0x09,
                0x08,
                0x16,
                0x0A,
                0x3F,
                0x78,
                0x4C,
                0x09,
                0x0A,
                0x08,
                0x16,
                0x1A,
                0x0F,
            )
        )
        gamma_n = bytes(
            (
                0x00,
                0x16,
                0x19,
                0x03,
                0x0F,
                0x05,
                0x32,
                0x45,
                0x46,
                0x04,
                0x0E,
                0x0D,
                0x35,
                0x37,
                0x0F,
            )
        )

        self._write_cmd(0xE0)
        self._write_data(gamma_p)
        self._write_cmd(0xE1)
        self._write_data(gamma_n)

        self._write_cmd(0xC0)
        self._write_data(bytes((0x17, 0x15)))
        self._write_cmd(0xC1)
        self._write_data(bytes((0x41,)))
        self._write_cmd(0xC5)
        self._write_data(bytes((0x00, 0x12, 0x80)))

        self._write_cmd(0x36)
        self._write_data(bytes((0x28,)))
        self._write_cmd(0x3A)
        self._write_data(bytes((0x66,)))

        self._write_cmd(0xB0)
        self._write_data(bytes((0x00,)))
        self._write_cmd(0xB1)
        self._write_data(bytes((0xA0,)))
        self._write_cmd(0xB4)
        self._write_data(bytes((0x02,)))
        self._write_cmd(0xB6)
        self._write_data(bytes((0x02, 0x02, 0x3B)))
        self._write_cmd(0xB7)
        self._write_data(bytes((0xC6,)))
        self._write_cmd(0xF7)
        self._write_data(bytes((0xA9, 0x51, 0x2C, 0x82)))

        self._write_cmd(0x11)
        time.sleep_ms(120)
        self._write_cmd(0x29)
        time.sleep_ms(25)

    def _set_addr_window(self, x1, y1, w, h):
        x2 = x1 + w - 1
        y2 = y1 + h - 1
        self._write_cmd(0x2A)
        self._write_data(bytes((x1 >> 8, x1 & 0xFF, x2 >> 8, x2 & 0xFF)))
        self._write_cmd(0x2B)
        self._write_data(bytes((y1 >> 8, y1 & 0xFF, y2 >> 8, y2 & 0xFF)))

    def draw_pixel(self, x, y, color565):
        if x < 0 or y < 0 or x >= self.WIDTH or y >= self.HEIGHT:
            return
        px = _rgb565_to_rgb666(color565)
        self._set_addr_window(x, y, 1, 1)
        self._write_cmd(0x2C)
        self._write_data(px)

    def fill_rect(self, x, y, w, h, color565):
        xa = x
        ya = y
        xb = x + w - 1
        yb = y + h - 1
        if xa < 0:
            xa = 0
        if ya < 0:
            ya = 0
        if xb >= self.WIDTH:
            xb = self.WIDTH - 1
        if yb >= self.HEIGHT:
            yb = self.HEIGHT - 1
        rw = xb - xa + 1
        rh = yb - ya + 1
        if rw <= 0 or rh <= 0:
            return

        px = _rgb565_to_rgb666(color565)
        total = rw * rh
        chunk = 80
        buf = bytearray(3 * chunk)
        self._set_addr_window(xa, ya, rw, rh)
        self._write_cmd(0x2C)
        sent = 0
        while sent < total:
            n = total - sent
            if n > chunk:
                n = chunk
            for i in range(n):
                buf[i * 3] = px[0]
                buf[i * 3 + 1] = px[1]
                buf[i * 3 + 2] = px[2]
            self._write_data(memoryview(buf)[: n * 3])
            sent += n

    def fill_screen(self, color565):
        self.fill_rect(0, 0, self.WIDTH, self.HEIGHT, color565)

    def draw_text8(self, s, x, y, fg565=0xFFFF, bg565=0x0000):

        import framebuf

        s = str(s)
        w = min(self.WIDTH - x, 8 * len(s))
        h = 8
        if w <= 0:
            return
        buf = bytearray(w * h * 2)
        fb = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)
        fb.fill(bg565)
        fb.text(s, 0, 0, fg565)
        for yy in range(h):
            out = bytearray(w * 3)
            for xx in range(w):
                t = _rgb565_to_rgb666(fb.pixel(xx, yy))
                out[xx * 3] = t[0]
                out[xx * 3 + 1] = t[1]
                out[xx * 3 + 2] = t[2]
            self._set_addr_window(x, y + yy, w, 1)
            self._write_cmd(0x2C)
            self._write_data(out)
