"""ILI9488 test on SPI0. Enable SPI and install the packages in Board setup."""
import spidev
from gpiozero import DigitalOutputDevice
from ili9488 import ILI9488


def main():
    spi = spidev.SpiDev()
    pins = []
    try:
        spi.open(0, 0)
        spi.mode = 0
        spi.max_speed_hz = 8_000_000
        spi.no_cs = False  # Kernel owns CE0/BCM8. Do not claim it with gpiozero.
        for bcm in (25, 27, 18):
            pins.append(DigitalOutputDevice(bcm, initial_value=False))
        dc, rst, bl = pins
        display = ILI9488(spi, None, dc, rst, bl)
        display.init()
        display.fill_screen(0)
        for x, color in ((0, 0xF800), (160, 0x07E0), (320, 0x001F)):
            display.fill_rect(x, 0, 160, 240, color)
        display.draw_text8("HotSwap Arcade", 16, 270)
        input("Verify colors and text. Press Enter to turn the backlight off. ")
    except KeyboardInterrupt:
        pass
    finally:
        for pin in pins:
            pin.off()
            pin.close()
        spi.close()


if __name__ == "__main__":
    main()
