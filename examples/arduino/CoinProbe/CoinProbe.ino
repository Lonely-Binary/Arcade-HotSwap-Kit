/*  HotSwap Arcade Kit - coin probe: count the pulses one coin sends
    Nano:     Tools > Board Arduino Nano · Processor ATmega328P
    ESP32-S3: Tools > Board ESP32S3 Dev Module · USB CDC On Boot Enabled
              when the cable is in the board's native USB port
    Power the mainboard from its USB-C: the acceptor's 12 V comes from there.
    Serial Monitor at 115200. A pulse is the line pulled LOW.
    Guide: https://learn.lonelybinary.com/manuals/arcade/count-the-pulses  */

#include <Arduino.h>

#if defined(ARDUINO_AVR_NANO)
const uint8_t COIN_PINS[] = {A0};
const char *COIN_NAMES[] = {"COIN A0"};
#elif defined(CONFIG_IDF_TARGET_ESP32S3)
// COIN (header pin 19) lands on GPIO14, COUNTER (pin 18) on GPIO21.
// Watch both, and see which one your acceptor pulses. Never add them up.
const uint8_t COIN_PINS[] = {14,21};
const char *COIN_NAMES[] = {"COIN GPIO14", "COUNTER GPIO21"};
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
  // #region group
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
  // #endregion
  delay(1);
}
