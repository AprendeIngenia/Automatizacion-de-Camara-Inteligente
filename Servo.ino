#include <SoftwareSerial.h>
#include <Servo.h>

//Declaramos el servo
Servo servo;

//Declaramos la variable
char dato;
int angulo = 90;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  servo.attach(3);
  servo.write(angulo);
}

void loop() {
  while(Serial.available()){
    dato = Serial.read();
    delay(10);
    Serial.println(dato);
    switch(dato){
      case 'd':
      //Gira servo hacia la derecha
      angulo = angulo + 2;
      servo.write(angulo);
      break;
      
      case 'i':
      //Gira servo hacia la izquierda
      angulo = angulo - 2;
      servo.write(angulo);
      break;
      
      case 'p':
      //Parar el servo
      angulo = angulo;
      servo.write(angulo);
      break;
      }
   }
 }
