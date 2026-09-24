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

// Diagnostic only. Keep loop fast; no display or long delays here.
const uint8_t CHANNELS = sizeof(COIN_PINS) / sizeof(COIN_PINS[0]);
const unsigned long LOCKOUT_MS = 60, GROUP_MS = 200;
bool lastLow[CHANNELS], seen[CHANNELS];
unsigned long lastEdge[CHANNELS];
uint16_t pulses[CHANNELS];

void setup() {
  Serial.begin(115200);
  delay(1000);
  for (uint8_t i=0; i<CHANNELS; ++i) {
    pinMode(COIN_PINS[i], INPUT_PULLUP);
    lastLow[i] = digitalRead(COIN_PINS[i]) == LOW;
  }
  Serial.println("Coin probe ready. Insert one learned coin, then wait.");
}

void loop() {
  unsigned long now = millis();
  for (uint8_t i=0; i<CHANNELS; ++i) {
    if (pulses[i] && now-lastEdge[i] >= GROUP_MS) {
      Serial.print(COIN_NAMES[i]); Serial.print(": ");
      Serial.print(pulses[i]); Serial.println(" pulse(s)");
      pulses[i] = 0;
    }
    bool low = digitalRead(COIN_PINS[i]) == LOW;
    if (low && !lastLow[i] && (!seen[i] || now-lastEdge[i] >= LOCKOUT_MS)) {
      seen[i] = true;
      lastEdge[i] = now;
      if (pulses[i] < 65535) ++pulses[i];
    }
    lastLow[i] = low;
  }
  delay(1);
}
