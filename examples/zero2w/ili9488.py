"""ILI9488 480x320 SPI driver; adapted from the kit bench tests."""
from __future__ import annotations

import time
from typing import Any, Optional

_FONT8 = (
    b"\x00\x00\x00\x00\x00\x00\x00\x00"  # space
    b"\x18\x3c\x3c\x18\x18\x00\x18\x00"  # !
    b"\x36\x36\x00\x00\x00\x00\x00\x00"
    b"\x36\x36\x7f\x36\x7f\x36\x36\x00"
    b"\x0c\x3e\x03\x1e\x30\x1f\x0c\x00"
    b"\x00\x63\x33\x18\x0c\x66\x63\x00"
    b"\x1c\x36\x1c\x6e\x3b\x33\x6e\x00"
    b"\x06\x06\x03\x00\x00\x00\x00\x00"
    b"\x18\x0c\x06\x06\x06\x0c\x18\x00"
    b"\x06\x0c\x18\x18\x18\x0c\x06\x00"
    b"\x00\x66\x3c\xff\x3c\x66\x00\x00"
    b"\x00\x0c\x0c\x3f\x0c\x0c\x00\x00"
    b"\x00\x00\x00\x00\x00\x0c\x0c\x06"
    b"\x00\x00\x00\x3f\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x0c\x0c\x00"
    b"\x60\x30\x18\x0c\x06\x03\x01\x00"
    b"\x3e\x63\x73\x7b\x6f\x67\x3e\x00"  # 0
    b"\x0c\x0e\x0c\x0c\x0c\x0c\x3f\x00"
    b"\x1e\x33\x30\x1c\x06\x33\x3f\x00"
    b"\x1e\x33\x30\x1c\x30\x33\x1e\x00"
    b"\x38\x3c\x36\x33\x7f\x30\x78\x00"
    b"\x3f\x03\x1f\x30\x30\x33\x1e\x00"
    b"\x1c\x06\x03\x1f\x33\x33\x1e\x00"
    b"\x3f\x33\x30\x18\x0c\x0c\x0c\x00"
    b"\x1e\x33\x33\x1e\x33\x33\x1e\x00"
    b"\x1e\x33\x33\x3e\x30\x18\x0e\x00"
    b"\x00\x0c\x0c\x00\x00\x0c\x0c\x00"
    b"\x00\x0c\x0c\x00\x00\x0c\x0c\x06"
    b"\x18\x0c\x06\x03\x06\x0c\x18\x00"
    b"\x00\x00\x3f\x00\x00\x3f\x00\x00"
    b"\x06\x0c\x18\x30\x18\x0c\x06\x00"
    b"\x1e\x33\x30\x18\x0c\x00\x0c\x00"
    b"\x3e\x63\x7b\x7b\x7b\x03\x1e\x00"
    b"\x0c\x1e\x33\x33\x3f\x33\x33\x00"  # A
    b"\x3f\x66\x66\x3e\x66\x66\x3f\x00"
    b"\x3c\x66\x03\x03\x03\x66\x3c\x00"
    b"\x1f\x36\x66\x66\x66\x36\x1f\x00"
    b"\x7f\x46\x16\x1e\x16\x46\x7f\x00"
    b"\x7f\x46\x16\x1e\x16\x06\x0f\x00"
    b"\x3c\x66\x03\x03\x73\x66\x7c\x00"
    b"\x33\x33\x33\x3f\x33\x33\x33\x00"
    b"\x1e\x0c\x0c\x0c\x0c\x0c\x1e\x00"
    b"\x78\x30\x30\x30\x33\x33\x1e\x00"
    b"\x67\x66\x36\x1e\x36\x66\x67\x00"
    b"\x0f\x06\x06\x06\x46\x66\x7f\x00"
    b"\x63\x77\x7f\x7f\x6b\x63\x63\x00"
    b"\x63\x67\x6f\x7b\x73\x63\x63\x00"
    b"\x1c\x36\x63\x63\x63\x36\x1c\x00"
    b"\x3f\x66\x66\x3e\x06\x06\x0f\x00"
    b"\x1e\x33\x33\x33\x3b\x1e\x38\x00"
    b"\x3f\x66\x66\x3e\x36\x66\x67\x00"
    b"\x1e\x33\x07\x0e\x38\x33\x1e\x00"
    b"\x3f\x2d\x0c\x0c\x0c\x0c\x1e\x00"
    b"\x33\x33\x33\x33\x33\x33\x3f\x00"
    b"\x33\x33\x33\x33\x33\x1e\x0c\x00"
    b"\x63\x63\x63\x6b\x7f\x77\x63\x00"
    b"\x63\x63\x36\x1c\x1c\x36\x63\x00"
    b"\x33\x33\x33\x1e\x0c\x0c\x1e\x00"
    b"\x7f\x63\x31\x18\x4c\x66\x7f\x00"
    b"\x1e\x06\x06\x06\x06\x06\x1e\x00"
    b"\x03\x06\x0c\x18\x30\x60\x40\x00"
    b"\x1e\x18\x18\x18\x18\x18\x1e\x00"
    b"\x08\x1c\x36\x63\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\xff"
    b"\x0c\x0c\x18\x00\x00\x00\x00\x00"
    b"\x00\x00\x1e\x30\x3e\x33\x6e\x00"  # a
    b"\x07\x06\x06\x3e\x66\x66\x3b\x00"
    b"\x00\x00\x1e\x33\x03\x33\x1e\x00"
    b"\x38\x30\x30\x3e\x33\x33\x6e\x00"
    b"\x00\x00\x1e\x33\x3f\x03\x1e\x00"
    b"\x1c\x36\x06\x0f\x06\x06\x0f\x00"
    b"\x00\x00\x6e\x33\x33\x3e\x30\x1f"
    b"\x07\x06\x36\x6e\x66\x66\x67\x00"
    b"\x0c\x00\x0e\x0c\x0c\x0c\x1e\x00"
    b"\x30\x00\x30\x30\x30\x33\x33\x1e"
    b"\x07\x06\x66\x36\x1e\x36\x67\x00"
    b"\x0e\x0c\x0c\x0c\x0c\x0c\x1e\x00"
    b"\x00\x00\x33\x7f\x7f\x6b\x63\x00"
    b"\x00\x00\x1f\x33\x33\x33\x33\x00"
    b"\x00\x00\x1e\x33\x33\x33\x1e\x00"
    b"\x00\x00\x3b\x66\x66\x3e\x06\x0f"
    b"\x00\x00\x6e\x33\x33\x3e\x30\x78"
    b"\x00\x00\x3b\x6e\x66\x06\x0f\x00"
    b"\x00\x00\x3e\x03\x1e\x30\x1f\x00"
    b"\x08\x0c\x3e\x0c\x0c\x2c\x18\x00"
    b"\x00\x00\x33\x33\x33\x33\x6e\x00"
    b"\x00\x00\x33\x33\x33\x1e\x0c\x00"
    b"\x00\x00\x63\x6b\x7f\x7f\x36\x00"
    b"\x00\x00\x63\x36\x1c\x36\x63\x00"
    b"\x00\x00\x33\x33\x33\x3e\x30\x1f"
    b"\x00\x00\x3f\x19\x0c\x26\x3f\x00"
    b"\x38\x0c\x0c\x07\x0c\x0c\x38\x00"
    b"\x18\x18\x18\x00\x18\x18\x18\x00"
    b"\x07\x0c\x0c\x38\x0c\x0c\x07\x00"
    b"\x6e\x3b\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00"
)

def _rgb565_to_rgb666(color: int) -> bytes:
    r5 = (color >> 11) & 0x1F
    g6 = (color >> 5) & 0x3F
    b5 = color & 0x1F
    return bytes((b5 << 3, g6 << 2, r5 << 3))

def _sleep_ms(ms: float) -> None:
    time.sleep(ms / 1000.0)

class ILI9488:
    WIDTH = 480
    HEIGHT = 320

    def __init__(self, spi: Any, cs: Any, dc: Any, rst: Any, bl: Optional[Any] = None):

        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.bl = bl

    def _pin_set(self, pin: Any, value: int) -> None:
        if pin is None:
            return
        if callable(pin):
            pin(value)
        else:
            pin.value = value

    def _spi_write(self, data: bytes | memoryview | bytearray) -> None:

        buf = bytes(data) if not isinstance(data, (bytes, bytearray)) else data
        if hasattr(self.spi, "writebytes2"):
            self.spi.writebytes2(buf)
        else:
            self.spi.writebytes(list(buf))

    def _hw_reset(self) -> None:
        if self.rst is None:
            return
        self._pin_set(self.rst, 1)
        _sleep_ms(5)
        self._pin_set(self.rst, 0)
        _sleep_ms(20)
        self._pin_set(self.rst, 1)
        _sleep_ms(120)

    def _write_cmd(self, c: int) -> None:
        self._pin_set(self.dc, 0)
        self._pin_set(self.cs, 0)
        self._spi_write(bytes((c,)))
        self._pin_set(self.cs, 1)

    def _write_data(self, buf: bytes | memoryview | bytearray) -> None:
        self._pin_set(self.dc, 1)
        self._pin_set(self.cs, 0)
        self._spi_write(buf)
        self._pin_set(self.cs, 1)

    def init(self) -> None:
        if self.bl is not None:
            self._pin_set(self.bl, 1)

        self._pin_set(self.cs, 1)
        self._pin_set(self.dc, 0)
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
        _sleep_ms(120)
        self._write_cmd(0x29)
        _sleep_ms(25)

    def _set_addr_window(self, x1: int, y1: int, w: int, h: int) -> None:
        x2 = x1 + w - 1
        y2 = y1 + h - 1
        self._write_cmd(0x2A)
        self._write_data(bytes((x1 >> 8, x1 & 0xFF, x2 >> 8, x2 & 0xFF)))
        self._write_cmd(0x2B)
        self._write_data(bytes((y1 >> 8, y1 & 0xFF, y2 >> 8, y2 & 0xFF)))

    def draw_pixel(self, x: int, y: int, color565: int) -> None:
        if x < 0 or y < 0 or x >= self.WIDTH or y >= self.HEIGHT:
            return
        px = _rgb565_to_rgb666(color565)
        self._set_addr_window(x, y, 1, 1)
        self._write_cmd(0x2C)
        self._write_data(px)

    def fill_rect(self, x: int, y: int, w: int, h: int, color565: int) -> None:
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
        chunk = 512
        buf = bytearray(3 * chunk)
        for i in range(chunk):
            buf[i * 3] = px[0]
            buf[i * 3 + 1] = px[1]
            buf[i * 3 + 2] = px[2]

        self._set_addr_window(xa, ya, rw, rh)
        self._write_cmd(0x2C)
        sent = 0
        while sent < total:
            n = total - sent
            if n > chunk:
                n = chunk
            self._write_data(memoryview(buf)[: n * 3])
            sent += n

    def fill_screen(self, color565: int) -> None:
        self.fill_rect(0, 0, self.WIDTH, self.HEIGHT, color565)

    def draw_text8(
        self, s: str, x: int, y: int, fg565: int = 0xFFFF, bg565: int = 0x0000
    ) -> None:

        s = str(s)
        max_chars = max(0, (self.WIDTH - x) // 8)
        if max_chars <= 0:
            return
        s = s[:max_chars]
        w = 8 * len(s)
        h = 8
        fg = _rgb565_to_rgb666(fg565)
        bg = _rgb565_to_rgb666(bg565)

        for yy in range(h):
            out = bytearray(w * 3)
            for ci, ch in enumerate(s):
                code = ord(ch)
                if code < 32 or code > 127:
                    code = 63  # '?'
                glyph = _FONT8[(code - 32) * 8 + yy]
                for xx in range(8):
                    on = (glyph >> xx) & 1
                    t = fg if on else bg
                    o = (ci * 8 + xx) * 3
                    out[o] = t[0]
                    out[o + 1] = t[1]
                    out[o + 2] = t[2]
            self._set_addr_window(x, y + yy, w, 1)
            self._write_cmd(0x2C)
            self._write_data(out)
