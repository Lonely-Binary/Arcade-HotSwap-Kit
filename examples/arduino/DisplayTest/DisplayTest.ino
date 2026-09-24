// ILI9488 only. ESP32-S3 adapter pinout; start with the color test.
#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <driver/spi_master.h>
#include <esp_err.h>
#if !defined(CONFIG_IDF_TARGET_ESP32S3)
#error "This display example requires ESP32-S3."
#endif
class ILI9488_SpiBus : public Adafruit_GFX {
 public:
  ILI9488_SpiBus(int8_t cs, int8_t dc, int8_t rst)
      : Adafruit_GFX(480, 320), _cs(cs), _dc(dc), _rst(rst) {}

  bool begin(spi_host_device_t host, uint32_t clock_hz = 8000000) {
    if (_dev != nullptr) return true;

    pinMode(_dc, OUTPUT);
    digitalWrite(_dc, LOW);
    if (_rst >= 0) {
      pinMode(_rst, OUTPUT);
      digitalWrite(_rst, HIGH);
      delay(5);
      digitalWrite(_rst, LOW);
      delay(20);
      digitalWrite(_rst, HIGH);
      delay(120);
    }

    spi_device_interface_config_t devcfg = {};
    devcfg.clock_speed_hz = (int)clock_hz;
    devcfg.mode = 0;
    devcfg.spics_io_num = _cs;
    devcfg.queue_size = 4;
    devcfg.cs_ena_posttrans = 2;

    esp_err_t err = spi_bus_add_device(host, &devcfg, &_dev);
    if (err != ESP_OK) {
      Serial.printf("[LCD] spi_bus_add_device failed: %s\n", esp_err_to_name(err));
      return false;
    }

    static const uint8_t gamma_p[] = {0x00, 0x03, 0x09, 0x08, 0x16, 0x0A, 0x3F, 0x78, 0x4C,
                                      0x09, 0x0A, 0x08, 0x16, 0x1A, 0x0F};
    static const uint8_t gamma_n[] = {0x00, 0x16, 0x19, 0x03, 0x0F, 0x05, 0x32, 0x45, 0x46,
                                      0x04, 0x0E, 0x0D, 0x35, 0x37, 0x0F};

    writeCmd(0xE0);
    writeData(gamma_p, sizeof(gamma_p));
    writeCmd(0xE1);
    writeData(gamma_n, sizeof(gamma_n));

    writeCmd(0xC0);
    uint8_t c01[] = {0x17, 0x15};
    writeData(c01, 2);
    writeCmd(0xC1);
    uint8_t c11[] = {0x41};
    writeData(c11, 1);
    writeCmd(0xC5);
    uint8_t c51[] = {0x00, 0x12, 0x80};
    writeData(c51, 3);

    writeCmd(0x36);
    uint8_t mad = 0x28;
    writeData(&mad, 1);

    writeCmd(0x3A);
    uint8_t pix = 0x66;
    writeData(&pix, 1);

    writeCmd(0xB0);
    uint8_t b0[] = {0x00};
    writeData(b0, 1);
    writeCmd(0xB1);
    uint8_t b1[] = {0xA0};
    writeData(b1, 1);
    writeCmd(0xB4);
    uint8_t b4[] = {0x02};
    writeData(b4, 1);
    writeCmd(0xB6);
    uint8_t b6[] = {0x02, 0x02, 0x3B};
    writeData(b6, 3);
    writeCmd(0xB7);
    uint8_t b7[] = {0xC6};
    writeData(b7, 1);
    writeCmd(0xF7);
    uint8_t f7[] = {0xA9, 0x51, 0x2C, 0x82};
    writeData(f7, 4);

    writeCmd(0x11);
    delay(120);
    writeCmd(0x29);
    delay(25);
    return true;
  }



  void startWrite() override {
    if (_dev == nullptr || _busHeld) return;
    esp_err_t e = spi_device_acquire_bus(_dev, portMAX_DELAY);
    _busHeld = (e == ESP_OK);
  }

  void endWrite() override {
    if (_dev == nullptr || !_busHeld) return;
    spi_device_release_bus(_dev);
    _busHeld = false;
  }

  void drawPixel(int16_t x, int16_t y, uint16_t color) override {
    if (x < 0 || y < 0 || x >= _width || y >= _height) return;
    uint8_t px[3];
    rgb565toRgb666(color, px);
    setAddrWindow((uint16_t)x, (uint16_t)y, 1, 1);
    writeCmd(0x2C);
    writeData(px, 3);
  }

  void fillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color) override {
    int16_t xa = x, ya = y, xb = x + w - 1, yb = y + h - 1;
    if (xa < 0) xa = 0;
    if (ya < 0) ya = 0;
    if (xb >= _width) xb = _width - 1;
    if (yb >= _height) yb = _height - 1;
    w = xb - xa + 1;
    h = yb - ya + 1;
    if (w <= 0 || h <= 0) return;

    uint8_t px[3];
    rgb565toRgb666(color, px);
    setAddrWindow((uint16_t)xa, (uint16_t)ya, (uint16_t)w, (uint16_t)h);
    writeCmd(0x2C);

    const uint32_t total = (uint32_t)w * (uint32_t)h;


    const uint32_t chunkPixels = 2048u;
    static uint8_t chunkBuf[3 * 2048];
    uint32_t sent = 0;
    while (sent < total) {
      uint32_t n = total - sent;
      if (n > chunkPixels) n = chunkPixels;
      for (uint32_t i = 0; i < n; i++) {
        chunkBuf[i * 3] = px[0];
        chunkBuf[i * 3 + 1] = px[1];
        chunkBuf[i * 3 + 2] = px[2];
      }
      writeData(chunkBuf, (size_t)n * 3u);
      sent += n;
    }
  }

 private:
  void writeCmd(uint8_t c) {
    digitalWrite(_dc, LOW);
    spi_transaction_t t = {};
    t.length = 8;
    t.tx_buffer = &c;
    ESP_ERROR_CHECK(spi_device_polling_transmit(_dev, &t));
  }

  void writeData(const uint8_t *data, size_t len) {
    if (len == 0) return;
    digitalWrite(_dc, HIGH);
    spi_transaction_t t = {};
    t.length = (uint32_t)len * 8;
    t.tx_buffer = const_cast<uint8_t *>(data);
    ESP_ERROR_CHECK(spi_device_polling_transmit(_dev, &t));
  }

  void setAddrWindow(uint16_t x1, uint16_t y1, uint16_t w, uint16_t h) {
    uint16_t x2 = (uint16_t)(x1 + w - 1);
    uint16_t y2 = (uint16_t)(y1 + h - 1);
    writeCmd(0x2A);
    uint8_t xa[] = {(uint8_t)(x1 >> 8), (uint8_t)(x1 & 0xFF), (uint8_t)(x2 >> 8), (uint8_t)(x2 & 0xFF)};
    writeData(xa, 4);
    writeCmd(0x2B);
    uint8_t ya[] = {(uint8_t)(y1 >> 8), (uint8_t)(y1 & 0xFF), (uint8_t)(y2 >> 8), (uint8_t)(y2 & 0xFF)};
    writeData(ya, 4);
  }

  static void rgb565toRgb666(uint16_t color, uint8_t out[3]) {
    uint8_t r5 = (color >> 11) & 0x1F;
    uint8_t g6 = (color >> 5) & 0x3F;
    uint8_t b5 = color & 0x1F;
    out[0] = (uint8_t)(b5 << 3);
    out[1] = (uint8_t)(g6 << 2);
    out[2] = (uint8_t)(r5 << 3);
  }

  int8_t _cs, _dc, _rst;
  spi_device_handle_t _dev = nullptr;
  bool _busHeld = false;
};


ILI9488_SpiBus tft(10, 2, 42);
void setup() {
  Serial.begin(115200);
  pinMode(41, OUTPUT);
  digitalWrite(41, HIGH);
  spi_bus_config_t bus = {};
  bus.mosi_io_num=11; bus.miso_io_num=13; bus.sclk_io_num=12;
  bus.quadwp_io_num=-1; bus.quadhd_io_num=-1;
  bus.max_transfer_sz=65536;
  ESP_ERROR_CHECK(spi_bus_initialize(SPI3_HOST, &bus, SPI_DMA_CH_AUTO));
  if (!tft.begin(SPI3_HOST, 8000000)) return;
  tft.fillScreen(0);
  tft.fillRect(0,0,160,240,0xF800);
  tft.fillRect(160,0,160,240,0x07E0);
  tft.fillRect(320,0,160,240,0x001F);
  tft.setTextColor(0xFFFF); tft.setTextSize(2);
  tft.setCursor(16,270); tft.print("HotSwap Arcade");
  Serial.println("Test pattern sent. Verify colors and text on the screen.");
}
void loop() {}
