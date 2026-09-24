#include <Arduino.h>

#if defined(ARDUINO_AVR_NANO)
const uint8_t INPUT_PINS[] = {2,3,4,5,6,7,8,9,10,11,12,A4,A3,A2};
const uint8_t INPUT_MODE = INPUT; // Mainboard provides 10k pull-downs.
const uint8_t COIN_PINS[] = {A0};
const char *COIN_NAMES[] = {"A0"};
#elif defined(CONFIG_IDF_TARGET_ESP32S3)
const uint8_t INPUT_PINS[] = {4,5,6,7,15,16,17,18,8,40,39,38,9,47};
const uint8_t INPUT_MODE = INPUT_PULLDOWN;
// PCB export: COIN=14; original bench test: 21. Observe both.
const uint8_t COIN_PINS[] = {14,21};
const char *COIN_NAMES[] = {"GPIO14", "GPIO21"};
#else
#error "Select classic Arduino Nano or ESP32S3 Dev Module."
#endif

const char *NAMES[] = {"KEY1","KEY2","KEY3","KEY4","KEY5","KEY6","KEY7",
                       "KEY8","KEY9","KEY10","UP","DOWN","LEFT","RIGHT"};
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
  Serial.println("Input monitor ready. Press a button or move the joystick.");
}

void loop() {
  unsigned long now = millis();
  for (uint8_t i=0; i<14; ++i) {
    bool value = digitalRead(INPUT_PINS[i]) == HIGH;
    if (value != raw[i]) { raw[i] = value; changed[i] = now; }
    if (value != stable[i] && now - changed[i] >= 30) {
      stable[i] = value;
      Serial.print(NAMES[i]);
      Serial.println(value ? " pressed" : " released");
    }
  }
  delay(1);
}
