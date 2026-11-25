#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
}

void loop() {
  int count = WiFi.scanNetworks();
  if (count < 0) Serial.printf("Scan failed: %d\n", count);
  else Serial.printf("Found %d network(s)\n", count);
  WiFi.scanDelete();
  delay(10000);
}
