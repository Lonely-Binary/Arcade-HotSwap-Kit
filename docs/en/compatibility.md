# Hardware and software compatibility

[Home](../../README.md) · [Pin tables](pin-reference.md)

## Coin input differences

The mainboard netlist routes **COUNTER to header pin 18** and **COIN to pin 19**. Tracing these positions through the adapter exports gives:

| Adapter | COIN, header 19 | COUNTER, header 18 | Original test used |
| --- | --- | --- | --- |
| Nano | A0 | A1 | A0 |
| ESP32-S3 | GPIO14 | GPIO21 | GPIO21 |
| Pico / Pico 2 | GP28 | GP27 | GP28 |
| Zero 2 W | BCM26 | BCM24 | BCM24 |

The ESP32-S3 and Zero 2 W test programs therefore observe the **COUNTER route in these exports**. This may reflect a wiring or board-revision difference; the files alone do not establish which applies to your physical kit.

Run the [coin probe](04-coins.md), then use the verified input in your project. With all power disconnected, continuity checks from the labeled mainboard connector through the adapter can resolve a revision mismatch. Do not change wiring based only on an older program's variable name.

Sources: [mainboard netlist](../../hardware/netlists/arcade-mainboard_netlist_2026-09-24.tel), [ESP32-S3](../../hardware/netlists/arcade-esp32-s3_netlist_2026-09-24.tel), [Zero 2 W](../../hardware/netlists/arcade-zero2w_netlist_2026-09-24.tel).

## Displays

The supplied display tests use an **ILI9488, 480 × 320** driver. The [display kit listing](https://www.amazon.com/dp/B0GR4HRVV2) names **ST7735S, ST7789 and ST7796** controllers. Treat those as separate driver targets; equal screen size or FPC count does not establish compatibility.

The Nano adapter does not route the display pins. The Pico layout uses GP4/GP5/GP6 as MOSI/SCK/MISO; use **SoftSPI** for this arrangement. Zero 2 W uses hardware SPI0. A successful write-only SPI transaction does not identify or verify a connected screen.

## Power

The original quick-reference PDF describes V(MCU) as a logic reference. In the mainboard netlist, this is the VCC rail feeding switch contacts, pull-ups and FPC pin 2. It is not a general-purpose 12 V-to-GPIO level converter. Use the matched adapter and supplied acceptor cable; independently verify replacement peripherals.

## Example status

The tutorial examples use the provided pin maps and display initialization sequences. Compilation and host-side logic checks do not replace a hardware test. Verify input mapping, pulse timing and display output on your particular kit before using a project unattended.
