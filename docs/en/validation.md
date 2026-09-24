# Validation

[Home](../../README.md)

## Before using a new build

| Check | Expected result |
| --- | --- |
| Each button | One press and one release event |
| Each joystick direction | Correct name; diagonals may report two |
| Five identical learned coins | Five separate groups, identical pulse counts |
| Unlearned coin | No credit |
| Start with zero credit | Round does not begin |
| Start with one credit | One credit spent, one round begins |
| Hold the score button | Score increases once |
| Time expires | Further hits do not change the completed round |
| Display test | Distinct color bars and readable text |
| Restart | Documented startup behavior; RAM credits reset |

## Software checks

| Check | Result |
| --- | --- |
| Nano InputMonitor + CoinProbe | Compiled with Arduino AVR Boards 1.8.8 |
| ESP32-S3 InputMonitor + CoinProbe + DisplayTest | Compiled with Arduino-ESP32 3.3.10 |
| DisplayTest graphics dependency | Adafruit GFX Library 1.12.6, Adafruit BusIO 1.17.4 |
| Pico logic | 12 host-side tests passed |
| Documentation | Local links, image loading, SVG rendering and Python syntax checked |
| Physical hardware | New tutorial examples still require an on-device run |

Run the documentation and logic checks with desktop Python:

```bash
python3 tools/check_repository.py
python3 tools/test_logic.py
```

Arduino compile commands:

```bash
arduino-cli compile --fqbn arduino:avr:nano examples/arduino/InputMonitor
arduino-cli compile --fqbn arduino:avr:nano examples/arduino/CoinProbe
arduino-cli compile --fqbn esp32:esp32:esp32s3 examples/arduino/InputMonitor
arduino-cli compile --fqbn esp32:esp32:esp32s3 examples/arduino/CoinProbe
arduino-cli compile --fqbn esp32:esp32:esp32s3 examples/arduino/DisplayTest
```

The checks do not simulate the analog signal path, power supply, display controller or physical wiring. Complete the hardware checks above on your kit.
