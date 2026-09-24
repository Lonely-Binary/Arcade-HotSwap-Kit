"""Run on Pico / Pico 2 with arcade.py on the board."""
from time import sleep_ms
from arcade import Button, INPUT_PINS, INPUT_NAMES

buttons = [Button(gpio) for gpio in INPUT_PINS]
print("Input monitor ready. Press a button or move the joystick.")
while True:
    for name, button in zip(INPUT_NAMES, buttons):
        event = button.poll()
        if event:
            print(name, "pressed" if event == 1 else "released")
    sleep_ms(1)
