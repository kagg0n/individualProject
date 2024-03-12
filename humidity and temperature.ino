#include "DHT.h"
#include <Gyver433.h>

#define DHTPIN 3 // Номер пина датчика
DHT dht(DHTPIN, DHT11); //Инициация датчика
Gyver433_TX<2, G433_NOCRC> tx; // Инициализация передатчика
String humidity = "humi";
String temperature = "temp";
bool flag = 0;
void setup() {
  dht.begin();
  Serial.begin(9600);
}
void loop() {
  delay(2000); // 2 секунды задержки
  float h = dht.readHumidity(); //Измеряем влажность
  float t = dht.readTemperature(); //Измеряем температуру
  humidity = humidity + h;
  temperature = temperature + t;
  char transmitHum[10];
  char transmitTemp[10];
  humidity.toCharArray(transmitHum, 10);
  temperature.toCharArray(transmitTemp, 10);
  if (flag == 0){
  tx.write((byte*)transmitHum, sizeof(transmitHum));
  flag = 1;
  }
  else{
  tx.write((byte*)transmitTemp, sizeof(transmitTemp));
  flag = 0;
  }
  delay(1000);
  Serial.print(humidity);
  humidity = "humi";
  temperature = "temp";
}