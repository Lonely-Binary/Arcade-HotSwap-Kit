"""Run on Raspberry Pi OS. GPIO numbers are BCM, not header positions."""
from time import monotonic, sleep
from gpiozero import DigitalInputDevice

PINS = (4, 5, 6, 12, 13, 16, 17, 19, 14, 15, 20, 21, 22, 23)
NAMES = tuple("KEY%d" % n for n in range(1, 11)) + ("UP", "DOWN", "LEFT", "RIGHT")


def main():
    buttons = []
    try:
        for pin in PINS:
            buttons.append(DigitalInputDevice(pin, pull_up=False))
        raw = [b.value for b in buttons]
        stable = raw.copy()
        changed = [monotonic()] * len(buttons)
        print("Input monitor ready. Press a button or move the joystick.")
        while True:
            now = monotonic()
            for i, button in enumerate(buttons):
                value = button.value
                if value != raw[i]:
                    raw[i], changed[i] = value, now
                if value != stable[i] and now - changed[i] >= 0.030:
                    stable[i] = value
                    print(NAMES[i], "pressed" if value else "released")
            sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        for button in buttons:
            button.close()


if __name__ == "__main__":
    main()
