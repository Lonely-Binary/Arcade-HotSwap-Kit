# Examples

[Home](../README.md) · [Handbook](https://learn.lonelybinary.com/p/arcade)

Run one example at a time. Disconnect power before changing hardware.

| Example | Nano | ESP32-S3 | Pico / Pico 2 | Zero 2 W |
| --- | --- | --- | --- | --- |
| Inputs | [Arduino](arduino/InputMonitor/InputMonitor.ino) | [Arduino](arduino/InputMonitor/InputMonitor.ino) | [MicroPython](pico/input_monitor.py) | [Python](zero2w/input_monitor.py) |
| Coin probe | [Arduino](arduino/CoinProbe/CoinProbe.ino) | [Arduino](arduino/CoinProbe/CoinProbe.ino) | [MicroPython](pico/coin_probe.py) | [Python](zero2w/coin_probe.py) |
| Credit game | — | — | [MicroPython](pico/credit_game.py) | — |
| ILI9488 test | — | [Arduino](arduino/DisplayTest/DisplayTest.ino) | [MicroPython](pico/display_test.py) | [Python](zero2w/display_test.py) |

## Files to copy

- **Arduino:** open the `.ino` inside its same-named folder. InputMonitor and CoinProbe select the Nano or ESP32-S3 pin map from the selected board.
- **Pico inputs, coin probe or game:** copy `arcade.py` and the chosen program to the Pico. For a display, also copy `ili9488.py`. The standalone display test needs only `display_test.py` and `ili9488.py`.
- **Zero 2 W:** keep the selected script and `ili9488.py` (for the screen test) in the same directory on the Pi. Use Python 3.10 or later and the OS packages in the setup guide.

The ILI9488 drivers and ESP32 display initialization are adapted from the kit's bench programs. The smaller lessons separate input, coin and display checks so each can be verified independently. Coin probes report pulse groups without assigning currency values.

## Validation

The repository checker verifies local documentation links, Python syntax and example input arrays against the adapter netlists. Host-side tests exercise debounce, pulse grouping and game credit rules. Arduino sketches are compiled for the supported target boards; see [tools/](../tools/check_repository.py). Hardware acceptance steps are listed at the end of each lesson.
