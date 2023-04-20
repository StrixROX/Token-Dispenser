#include <ESP32QRCodeReader.h>

ESP32QRCodeReader reader(CAMERA_MODEL_AI_THINKER);

void onQrCodeTask(void* pvParameters) {
  struct QRCodeData qrCodeData;

  while (true) {
    if (reader.receiveQrCode(&qrCodeData, 100)) {
      Serial.print("<qr>");
      if (qrCodeData.valid) {
        Serial.print("1");
        Serial.print((const char*)qrCodeData.payload);
      }
      else {
        Serial.print("0");
        Serial.print((const char*)qrCodeData.payload);
      }
      Serial.print("</qr>");
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  reader.setup();

  Serial.println("Setup QRCode Reader");

  reader.beginOnCore(1);

  Serial.println("Ready");

  xTaskCreate(onQrCodeTask, "onQrCode", 4 * 1024, NULL, 4, NULL);
}

void loop() {
  delay(100);
}