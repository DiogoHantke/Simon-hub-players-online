#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* WIFI_SSID = "SEU_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA";

// Exemplo: http://192.168.0.10:5000/score
const char* SCORE_ENDPOINT = "http://192.168.0.10:5000/score";

String serialBuffer;
unsigned long lastWiFiAttempt = 0;

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  unsigned long now = millis();
  if (now - lastWiFiAttempt < 5000) {
    return;
  }

  lastWiFiAttempt = now;
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

bool sendScore(int score) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  WiFiClient client;
  HTTPClient http;

  if (!http.begin(client, SCORE_ENDPOINT)) {
    return false;
  }

  http.addHeader("Content-Type", "application/json");
  String payload = String("{\"score_player\":") + String(score) + "}";

  int httpCode = http.POST(payload);
  String response = http.getString();
  http.end();

  return httpCode >= 200 && httpCode < 300;
}

void processLine(String line) {
  line.trim();

  if (!line.startsWith("points:")) {
    return;
  }

  String value = line.substring(7);
  value.trim();
  int score = value.toInt();

  for (int attempt = 0; attempt < 5; attempt++) {
    connectWiFi();

    unsigned long waitStart = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - waitStart < 5000) {
      delay(100);
    }

    if (sendScore(score)) {
      return;
    }

    delay(1000);
  }
}

void setup() {
  Serial.begin(9600);
  serialBuffer.reserve(64);
  connectWiFi();
}

void loop() {
  connectWiFi();

  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      processLine(serialBuffer);
      serialBuffer = "";
    } else if (c != '\r') {
      serialBuffer += c;
    }
  }
}
