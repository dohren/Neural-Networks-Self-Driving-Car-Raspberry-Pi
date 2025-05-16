#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Motorpins für ESP32
const int r1 = 26, r2 = 27, l1 = 12, l2 = 14;
const int speedr = 25, speedl = 13;

// WLAN-Zugangsdaten
const char* ssid = "*******";
const char* password = "*********";

// MQTT
const char* mqtt_server = "lumabit-laptop-01";
const int mqtt_port = 1883;
const char* mqtt_topic = "robot1/motor/control";

WiFiClient espClient;
PubSubClient client(espClient);

// === Funktion zum Bewegen des Rovers (dauerhaft) ===
void move_rover(float speed, float turn) {
  speed *= 200;
  turn *= 140;

  float leftSpeed = speed - turn;
  float rightSpeed = speed + turn;

  leftSpeed = constrain(leftSpeed, -200, 200);
  rightSpeed = constrain(rightSpeed, -200, 200);

  // Linker Motor
  if (leftSpeed > 0) {
    digitalWrite(l1, LOW);
    digitalWrite(l2, HIGH);
    analogWrite(speedl, abs(leftSpeed));
  } else {
    digitalWrite(l1, HIGH);
    digitalWrite(l2, LOW);
    analogWrite(speedl, abs(leftSpeed));
  }

  // Rechter Motor
  if (rightSpeed > 0) {
    digitalWrite(r1, HIGH);
    digitalWrite(r2, LOW);
    analogWrite(speedr, abs(rightSpeed));
  } else {
    digitalWrite(r1, LOW);
    digitalWrite(r2, HIGH);
    analogWrite(speedr, abs(rightSpeed));
  }
}

// === Callback für MQTT-Nachrichten ===
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Nachricht empfangen [");
  Serial.print(topic);
  Serial.println("]");

  payload[length] = '\0';
  String message = String((char*)payload);
  Serial.println("Payload: " + message);

  StaticJsonDocument<128> doc;
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    Serial.println("Fehler beim Parsen des JSON:");
    Serial.println(error.c_str());
    return;
  }

  float speed = doc["speed"] | 0.0;
  float turn = doc["turn"] | 0.0;

  Serial.printf("Setze speed=%.2f, turn=%.2f\n", speed, turn);
  move_rover(speed, turn);
}

// === MQTT-Verbindung herstellen ===
void reconnect() {
  while (!client.connected()) {
    Serial.print("Verbinde mit MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Verbunden!");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("Fehler, rc=");
      Serial.print(client.state());
      Serial.println(" Warte 5 Sekunden...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Motorpins konfigurieren
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(speedl, OUTPUT);
  pinMode(speedr, OUTPUT);

  // WLAN verbinden
  Serial.print("Verbinde mit WLAN: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWLAN verbunden, IP: " + WiFi.localIP().toString());

  // MQTT einrichten
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
