#define BLYNK_TEMPLATE_ID "TMPL3U35_-eLU"
#define BLYNK_TEMPLATE_NAME "Soil Drip Irrigation System"
#define BLYNK_PRINT Serial

#include <WiFi.h>
#include <BlynkSimpleEsp32.h>
#include <HTTPClient.h>   // For Sterlite HTTP API

// Blynk credentials
char auth[] = "yA7sqwqgv0O-2Y4n8B-vY894aN-GeGwX";
char ssid[] = "Galaxy F23 5G 6ECB";
char pass[] = "21052004";

// Sterlite API details (replace with your actual API endpoint and token)
const char* sterlite_url = "https://api.sterlite.com/v1/devices/data"; 
const char* sterlite_token = "YOUR_STERLITE_TOKEN";  

BlynkTimer timer;

#define sensor 34      // Soil moisture sensor pin
#define relayPin 26    // Relay pin

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);

  // Connect to Blynk + WiFi
  Blynk.begin(auth, ssid, pass);

  // Run sensor check every second
  timer.setInterval(1000L, soilMoistureSensor);
}

// Manual ON/OFF from Blynk app
BLYNK_WRITE(V1) {
  if (param.asInt() == 1) {
    digitalWrite(relayPin, LOW);
  } else {
    digitalWrite(relayPin, HIGH);
  }
}

void soilMoistureSensor() {
  int value = analogRead(sensor);
  value = map(value, 0, 4095, 0, 100);  
  value = (value - 100) * -1;   // Convert to percentage

  // Send to Blynk
  Blynk.virtualWrite(V0, value);

  Serial.print("Moisture Value: ");
  Serial.println(value);

  // Auto irrigation control
  if (value < 30) {
    digitalWrite(relayPin, LOW);
  } else {
    digitalWrite(relayPin, HIGH);
  }

  // Send data to Sterlite Dashboard
  sendToSterlite(value);
}

void sendToSterlite(int moisture) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(sterlite_url);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + sterlite_token);

    // JSON payload (modify key name if Sterlite requires different field)
    String payload = "{\"soil_moisture\":" + String(moisture) + "}";

    int httpResponseCode = http.POST(payload);

    Serial.print("Sterlite response code: ");
    Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("WiFi not connected, cannot send to Sterlite");
  }
}

void loop() {
  Blynk.run();
  timer.run();
}