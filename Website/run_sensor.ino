#define RLOAD 22.0
// Calibration resistance at atmospheric CO2 level
#define RZERO 400 
#define DHTPIN 2
#define DHTTYPE 11
#include "DHT.h"
#include "MQ135.h" 
MQ135 gasSensor = MQ135(A0);
DHT dht(DHTPIN, DHTTYPE);
int val; 
int sensorPin = A0; 
int sensorValue = 0; 
void setup() { 
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  dht.begin(); 
} 
 
void loop() { 
  float ppm = gasSensor.getPPM(); 
  Serial.print(ppm);
  Serial.print(" ");
  Serial.print(dht.readTemperature());
  Serial.print(" ");
  Serial.println(dht.readHumidity()); 
  delay(1000); 
} 
