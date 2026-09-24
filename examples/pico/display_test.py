"""ILI9488 color bars. Copy ili9488.py to the Pico first."""
from machine import Pin, SoftSPI
from ili9488 import ILI9488

spi = SoftSPI(baudrate=1_000_000, polarity=0, phase=0,
              sck=Pin(5), mosi=Pin(4), miso=Pin(6))
display = ILI9488(spi, Pin(3), Pin(7), Pin(8), Pin(9))
display.init()
display.fill_screen(0)
for x, color in ((0, 0xF800), (160, 0x07E0), (320, 0x001F)):
    display.fill_rect(x, 0, 160, 240, color)
display.draw_text8("HotSwap Arcade", 16, 270)
print("Test pattern sent. Verify colors and text on the screen.")
