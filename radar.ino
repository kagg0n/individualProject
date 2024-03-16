#include <Gyver433.h>

Gyver433_TX<2, G433_NOCRC> tx;
int doplerPin = 6;

String dopler = "rada";
int previous = 0;
void setup() {
  
 // Serial.begin(9600);
  pinMode(doplerPin, INPUT);
}


void loop() {

  int SensorVal = digitalRead(doplerPin);
  dopler = dopler + SensorVal;
  char transmitDopl[10];
  dopler.toCharArray(transmitDopl, 10);

  if (SensorVal != previous){
    previous = SensorVal;
  tx.write((byte*)transmitDopl, sizeof(transmitDopl));
  
  }
  dopler = "rada";
  delay(700);
}