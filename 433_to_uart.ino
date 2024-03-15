#include <Gyver433.h>
#include <hardware/uart.h>

Gyver433_RX<6,20,G433_NOCRC> rx;

void setup(){
  Serial1.begin(115200);
}

void loop(){
  if (rx.tick()) {
    Serial1.write(rx.buffer,rx.size);
    delay(50);
    //Serial1.println();
  }
}