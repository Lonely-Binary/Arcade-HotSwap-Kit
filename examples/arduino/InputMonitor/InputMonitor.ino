/*  HotSwap Arcade Kit - input monitor: every button and joystick direction
    Nano:     Tools > Board Arduino Nano · Processor ATmega328P
              (try "ATmega328P (Old Bootloader)" if the upload times out)
    ESP32-S3: Tools > Board ESP32S3 Dev Module · USB CDC On Boot Enabled
              when the cable is in the board's native USB port
    Serial Monitor at 115200. Pressed reads HIGH: each input has a 10k
    pull-down on the mainboard, and the button connects it to V(MCU).
    Guide: https://learn.lonelybinary.com/manuals/arcade/press-a-button  */

#include <Arduino.h>

#if defined(ARDUINO_AVR_NANO)
const uint8_t INPUT_PINS[] = {2,3,4,5,6,7,8,9,10,11,12,A4,A3,A2};
const uint8_t INPUT_MODE = INPUT; // Mainboard provides 10k pull-downs.
#elif defined(CONFIG_IDF_TARGET_ESP32S3)
const uint8_t INPUT_PINS[] = {4,5,6,7,15,16,17,18,8,40,39,38,9,47};
const uint8_t INPUT_MODE = INPUT_PULLDOWN;
#else
#error "Select classic Arduino Nano or ESP32S3 Dev Module."
#endif

const char *NAMES[] = {"KEY1", "KEY2", "KEY3", "KEY4", "KEY5",
                       "KEY6", "KEY7", "KEY8", "KEY9", "KEY10",
                       "UP", "DOWN", "LEFT", "RIGHT"};
bool raw[14], stable[14];
unsigned long changed[14];

void setup() {
  Serial.begin(115200);
  delay(1000);
  for (uint8_t i=0; i<14; ++i) {
    pinMode(INPUT_PINS[i], INPUT_MODE);
    raw[i] = stable[i] = digitalRead(INPUT_PINS[i]) == HIGH;
    changed[i] = millis();
  }
  Serial.println("Ready. Press a button or push the stick.");
}

void loop() {
  unsigned long ms = millis();
  // #region debounce
  for (uint8_t i=0; i<14; ++i) {
    bool value = digitalRead(INPUT_PINS[i]) == HIGH;
    if (value != raw[i]) { raw[i] = value; changed[i] = ms; }
    if (value != stable[i] && ms - changed[i] >= 30) {
      stable[i] = value;
      Serial.print(NAMES[i]);
      Serial.println(value ? " pressed" : " released");
    }
  }
  // #endregion
  delay(1);
}
