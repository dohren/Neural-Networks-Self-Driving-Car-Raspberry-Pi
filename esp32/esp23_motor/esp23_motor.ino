#include <Arduino.h>
#include <WiFi.h>

// Motorpins für ESP32
const int r1 = 26, r2 = 27, l1 = 12, l2 = 14;
const int speedr = 25, speedl = 13;

// WiFi-Einstellungen
const char* ssid = "ROS";
const char* password = "robot123";

WiFiServer server(80);

// Funktion zum Bewegen des Rovers
void move_rover(float speed, float turn, float duration) {
  speed *= 200;
  turn *= 140;

  float leftSpeed = speed - turn;
  float rightSpeed = speed + turn;

  // Begrenzung der Geschwindigkeit auf -100 bis 100
  leftSpeed = constrain(leftSpeed, -100, 100);
  rightSpeed = constrain(rightSpeed, -100, 100);

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

  // Wartezeit für die Dauer der Bewegung
  if (duration > 0) {
    delay(duration * 1000);
    // Stoppe die Motoren nach Ablauf der Zeit
    analogWrite(speedl, 0);
    analogWrite(speedr, 0);
  }
}

// Funktion zum Parsen von Parametern aus der URL
float getParam(String request, String paramName) {
  int paramStart = request.indexOf(paramName + "=");
  if (paramStart == -1) {
    return 0.0; // Standardwert, wenn der Parameter nicht gefunden wird
  }
  int valueStart = paramStart + paramName.length() + 1;
  int valueEnd = request.indexOf("&", valueStart);
  if (valueEnd == -1) {
    valueEnd = request.indexOf(" ", valueStart);
  }
  String valueString = request.substring(valueStart, valueEnd);
  return valueString.toFloat();
}

void setup() {
  Serial.begin(115200);

  // Motorpins als Ausgang definieren
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(speedl, OUTPUT);
  pinMode(speedr, OUTPUT);

  // WiFi-Verbindung herstellen
  Serial.print("Verbinde mit WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi verbunden!");
  Serial.print("IP-Adresse: ");
  Serial.println(WiFi.localIP());

  // Webserver starten
  server.begin();
  Serial.println("Webserver gestartet!");
}

void loop() {
  // Webserver-Client
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Neuer Client verbunden!");

    String request = client.readStringUntil('\r');
    Serial.println("Anfrage: " + request);

    // Dynamische Parameter aus der URL parsen
    float speed = getParam(request, "speed");
    float turn = getParam(request, "turn");
    float time = getParam(request, "t"); // Optionaler Parameter 't' (Standardwert 0)

    Serial.print("Speed: ");
    Serial.println(speed);
    Serial.print("Turn: ");
    Serial.println(turn);
    Serial.print("Time: ");
    Serial.println(time);

    // Rover bewegen
    move_rover(speed, turn, time);

    // Einfache HTTP-Antwort ohne Body
    client.println("HTTP/1.1 200 OK");
    client.println();
    client.stop();
    Serial.println("Client getrennt.");
  }
}
