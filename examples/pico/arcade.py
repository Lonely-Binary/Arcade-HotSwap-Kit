"""Inputs for the HotSwap Pico adapter. Copy this file beside each example."""
from machine import Pin, disable_irq, enable_irq
from time import ticks_ms, ticks_diff
import micropython

micropython.alloc_emergency_exception_buf(100)
INPUT_PINS = (16, 17, 18, 19, 20, 21, 15, 14, 13, 12, 22, 11, 10, 26)
INPUT_NAMES = tuple("KEY%d" % n for n in range(1, 11)) + (
    "UP", "DOWN", "LEFT", "RIGHT"
)


class Button:
    def __init__(self, gpio):
        self.pin = Pin(gpio, Pin.IN, Pin.PULL_DOWN)
        self.raw = self.stable = self.pin.value()
        self.changed = ticks_ms()

    def poll(self):
        """Return 1 on press, -1 on release, 0 when unchanged."""
        now = ticks_ms()
        value = self.pin.value()
        if value != self.raw:
            self.raw = value
            self.changed = now
        if value != self.stable and ticks_diff(now, self.changed) >= 30:
            self.stable = value
            return 1 if value else -1
        return 0


class CoinInput:
    """Low pulses; group after 200 ms idle. Counts above 10 are invalid (11)."""
    def __init__(self, gpio=28):
        self.pin = Pin(gpio, Pin.IN, Pin.PULL_UP)
        self.count = 0
        self.last = 0
        self.seen = False
        # Preallocated queue: no list allocation in a hard interrupt.
        self.queue = [0] * 8
        self.read = self.write = 0
        self.overflow = False
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._edge, hard=True)

    def _edge(self, pin):
        now = ticks_ms()
        gap = ticks_diff(now, self.last)
        if self.seen and gap < 60:
            return
        if self.count and gap >= 200:
            nxt = (self.write + 1) % 8
            if nxt == self.read:
                self.overflow = True
            else:
                self.queue[self.write] = self.count
                self.write = nxt
            self.count = 0
        self.seen = True
        self.last = now
        if self.count < 11:
            self.count += 1

    def poll(self):
        """Return a complete group, 0 if waiting, or -1 if queue overflowed."""
        irq = disable_irq()
        try:
            if self.overflow:
                self.overflow = False
                self.read = self.write
                self.count = 0
                return -1
            if self.read != self.write:
                count = self.queue[self.read]
                self.read = (self.read + 1) % 8
                return count
            if self.count and ticks_diff(ticks_ms(), self.last) >= 200:
                count = self.count
                self.count = 0
                return count
            return 0
        finally:
            enable_irq(irq)

    def close(self):
        self.pin.irq(handler=None)


def make_display():
    """Optional ILI9488 display using this adapter's software SPI pin map."""
    from machine import SoftSPI
    from ili9488 import ILI9488
    spi = SoftSPI(baudrate=1_000_000, polarity=0, phase=0,
                  sck=Pin(5), mosi=Pin(4), miso=Pin(6))
    display = ILI9488(spi, Pin(3), Pin(7), Pin(8), Pin(9))
    display.init()
    display.fill_screen(0)
    return display
