#include <Gyver433.h>
Gyver433_TX<2, G433_NOCRC> tx;

String lightSend = "ligh";
int temt6000Pin = 26;                        // Создаем переменную и указываем вывод
float light;                                 // Создаем переменную
int light_value;                             // Создаем переменную 
 
void setup() 
{
  Serial.begin(115200);                        // Открываем последовательную связь

  pinMode(temt6000Pin, INPUT);                 // Устанавливаем вывод как вход 

}
 
void loop() 
{
light_value = analogRead(temt6000Pin); 
light = light_value * 0.0976;    
lightSend = lightSend + light;
Serial.println(lightSend);
char transmitLight[10];
lightSend.toCharArray(transmitLight,10);
Serial.println(transmitLight);
tx.write((byte*)transmitLight,sizeof(transmitLight));
lightSend = "ligh";
delay(500);                                  
}