# Troubleshooting

[Home](../../README.md) · [Pin reference](pin-reference.md)

| Symptom | Check first |
| --- | --- |
| No power LED | Regulated 5 V supply, cable and mainboard USB-C connection |
| LED on, no program output | Development-board programming port, firmware, selected board/port and 115200 baud |
| Computer sees no board | USB data cable; mainboard USB-C is power-only |
| Nano upload fails | Classic Nano selected; try ATmega328P (Old Bootloader) if that matches your board |
| ESP32-S3 upload waits forever | Correct USB port; hold BOOT, tap RESET, release BOOT and retry; check board-specific USB settings |
| Pico appears as a USB drive | Install matching MicroPython UF2, then select the MicroPython interpreter in Thonny |
| `No module named machine` | The Pico program was run in desktop Python; select the Pico interpreter |
| `No module named arcade` | Copy `arcade.py` beside the Pico example on the board |
| Button permanently pressed | NO/NC switch terminals, connector offset and pin mapping |
| Nano input floats | Mainboard connection; its built-in pull-down is required by the input example |
| Joystick directions reversed | Use the input monitor and swap the matching direction leads with power off |
| KEY9/KEY10 fail on Zero 2 W | Disable serial login and serial hardware; reboot to release BCM14/15 |
| Acceptor rejects coins | Learn the coin using the exact acceptor's manual; check supply under load |
| Coin accepted but no count | Run the two-channel probe where applicable; check COIN vs COUNTER and low-pulse output mode |
| One coin counts incorrectly | Match group timeout and lockout to the acceptor pulse settings |
| Blank / white display | Controller type, FPC contact orientation, latch, supply, reset and backlight |
| `[LCD] OK` but blank screen in an old test | SPI writes can succeed without a connected display; the message is not hardware identification |
| Red and blue reversed | Driver color order; the supplied ILI9488 driver uses a particular BGR configuration |
| Garbled display | Reduce SPI speed; check FPC seating and cable length |
| `/dev/spidev0.0` missing | Enable SPI in `raspi-config`, then reboot |
| GPIO busy / permission denied | Stop the other GPIO program; verify `gpio` / `spi` groups and log in again |
| Resets when a coin is inserted | USB supply/cable voltage drop, short circuits and coin-acceptor load |

When reporting an issue, include the adapter, development-board model, board revision, exact example, full error text and a clear connector photo. For display issues, include the controller name; screen size alone is not enough.
