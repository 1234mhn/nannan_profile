#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <time.h>

// Replace with the exact phone hotspot name before uploading.
// Never put the hotspot password or webhook token in this file.
const char* WIFI_SSID = "YOUR_HOTSPOT_SSID";
const char* WEBHOOK_URL = "https://esp32.nannan2026.cn/hooks/agent";

// Let's Encrypt ISRG Root X1. TLS certificate validation stays enabled.
static const char ROOT_CA[] PROGMEM = R"PEM(
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
)PEM";

String readSecret(const char* prompt) {
  Serial.println(prompt);
  String value;
  while (true) {
    while (Serial.available()) {
      char c = (char)Serial.read();
      if (c == '\r') continue;
      if (c == '\n') {
        value.trim();
        if (value.length() > 0) return value;
      } else if (value.length() < 256) {
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

  String wifiPassword = readSecret("Enter hotspot password, then press Send:");
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(WIFI_SSID, wifiPassword.c_str());
  wifiPassword = "";

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

  Serial.println("Syncing clock for TLS certificate validation...");
  configTime(0, 0, "pool.ntp.org", "time.google.com");
  time_t now = time(nullptr);
  unsigned long timeStarted = millis();
  while (now < 1760000000 && millis() - timeStarted < 20000) {
    delay(500);
    now = time(nullptr);
  }
  if (now < 1760000000) {
    Serial.println("NTP_TIME_SYNC_FAILED");
    return;
  }
  Serial.println("NTP_TIME_SYNCED");

  String hookToken = readSecret("Enter the OpenClaw webhook token, then press Send:");
  WiFiClientSecure tlsClient;
  tlsClient.setCACert(ROOT_CA);
  tlsClient.setTimeout(15000);

  HTTPClient https;
  https.setTimeout(20000);
  if (!https.begin(tlsClient, WEBHOOK_URL)) {
    Serial.println("HTTPS_BEGIN_FAILED");
    return;
  }

  https.addHeader("Content-Type", "application/json");
  https.addHeader("Authorization", "Bearer " + hookToken);
  https.addHeader("Idempotency-Key", "esp32-s3-smoke-test-20261126-01");

  const char* payload =
      R"JSON({"message":"这是一条 ESP32-S3 端到端连通性测试。请仅回复“收到”，不要执行任何操作。","name":"ESP32-S3测试","agentId":"main","deliver":false})JSON";

  Serial.println("Sending HTTPS webhook request...");
  int status = https.POST((uint8_t*)payload, strlen(payload));
  Serial.print("HTTP_STATUS: ");
  Serial.println(status);
  if (status > 0) {
    String response = https.getString();
    Serial.println("RESPONSE:");
    Serial.println(response);
  } else {
    Serial.print("HTTPS_ERROR: ");
    Serial.println(https.errorToString(status));
  }

  https.end();
  hookToken = "";
}

void loop() {
  delay(10000);
}
