#include <WiFi.h>
#include <HTTPClient.h>

// Replace with the hotspot name before uploading. No password is stored here.
const char* ssid = "YOUR_HOTSPOT_SSID";

String readPassword() {
  Serial.println("Enter the current hotspot password, then press Enter:");
  String value;
  while (true) {
    while (Serial.available()) {
      char c = Serial.read();
      if (c == '\r') continue;
      if (c == '\n') {
        value.trim();
        if (value.length() > 0) return value;
      } else {
        value += c;
      }
    }
    delay(10);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1200);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);

  Serial.print("Target SSID: ");
  Serial.println(ssid);
  String password = readPassword();

  Serial.println("Connecting...");
  WiFi.begin(ssid, password.c_str());
  unsigned long started = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - started < 30000) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("WIFI_FAILED status=");
    Serial.println(WiFi.status());
    return;
  }

  Serial.println("WIFI_CONNECTED");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("RSSI: ");
  Serial.println(WiFi.RSSI());

  IPAddress resolved;
  if (WiFi.hostByName("example.com", resolved)) {
    Serial.print("DNS_OK example.com = ");
    Serial.println(resolved);
  } else {
    Serial.println("DNS_FAILED");
    return;
  }

  HTTPClient http;
  http.setTimeout(10000);
  if (http.begin("http://example.com/")) {
    int code = http.GET();
    Serial.print("HTTP_STATUS: ");
    Serial.println(code);
    http.end();
  } else {
    Serial.println("HTTP_BEGIN_FAILED");
  }
}

void loop() {
  delay(10000);
}
