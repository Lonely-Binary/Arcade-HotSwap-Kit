# HotSwap Arcade Kit

**One control panel. Four ways to build.**

Connect buttons, a joystick and a coin acceptor to one mainboard. Choose an MCU adapter, upload an example and build your first arcade project.

![HotSwap Arcade Kit](docs/assets/arcade_photo-4.jpg)

[Start here](docs/en/01-start.md) · [Choose your board](docs/en/02-boards.md) · [Pin reference](docs/en/pin-reference.md) · [Troubleshooting](docs/en/troubleshooting.md)

## Build it one step at a time

| Step | Make something work | What you need |
| --- | --- | --- |
| [1. Meet the kit](docs/en/01-start.md) | Identify connectors and assemble the mainboard | Kit + matching development board |
| [2. Set up your board](docs/en/02-boards.md) | Upload your first program | Computer + USB data cable |
| [3. Buttons and joystick](docs/en/03-inputs.md) | See every press and direction | No display or coin setup needed |
| [4. Your first coin](docs/en/04-coins.md) | Read a pulse group | Coin acceptor + sample coins |
| [5. A coin-operated game](docs/en/05-game.md) | Insert a coin, press Start, beat your score | Pico / Pico 2 + two buttons |
| [6. Add a display](docs/en/06-display.md) | Show text and color on an SPI screen | Compatible display, sold separately |
| [7. Build an enclosure](docs/en/07-build.md) | Turn the bench setup into your own machine | CAD files + your enclosure design |

## Choose your platform

| Platform | Language | Buttons + coin | Display route |
| --- | --- | --- | --- |
| Classic Arduino Nano / ATmega328P | Arduino C++ | Yes | Not routed on this adapter |
| ESP32-S3 | Arduino C++ | Yes | SPI |
| Raspberry Pi Pico / Pico 2 | MicroPython | Yes | Software SPI with this pin layout |
| Raspberry Pi Zero 2 W | Python on Raspberry Pi OS | Yes | Hardware SPI0 |

The adapter is the carrier board; the development board runs your program. Check your purchased bundle for included parts. Disconnect power before changing adapters or cables.

## In this repository

- [Examples](examples/README.md): small input tests, coin diagnostics, a complete game and display tests.
- [Hardware](hardware/README.md): schematics, connector maps and STEP/GLB models.
- [Compatibility notes](docs/en/compatibility.md): board revisions, coin-pin differences and display controllers.

**Start with the input test.** Use the coin probe to verify the ESP32-S3 or Zero 2 W coin input. Display examples target **ILI9488**; check your screen's controller before using them.

[Arcade kit](https://www.amazon.com/dp/B0HFM5Z5ZZ) · [Optional display kit](https://www.amazon.com/dp/B0GR4HRVV2) · [Lonely Binary](https://lonelybinary.com)
