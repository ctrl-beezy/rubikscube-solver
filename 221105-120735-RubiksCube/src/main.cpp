#include "motorContr.hpp"
#include "cubeparser.hpp"
#include <Arduino.h>
#include <Wire.h>
#include <string.h>

#define DIR 16
#define STEP 10
#define EN1 2
#define EN2 3
#define EN3 4
#define EN4 5
#define EN5 6
#define EN6 7

extern String Buffer;                                    //String erstellen, um serielle Daten Zwischenzuspeichern
extern int Rotationen;
extern bool busy;
extern int Zeit;
extern int cnt1;
extern int Drehungen;
movement movementList[50];
movement* lastmovement;
movement* amovement;

void setup() {
    pinMode(DIR, OUTPUT);
    pinMode(STEP, OUTPUT);
    pinMode(EN1, OUTPUT);
    pinMode(EN2, OUTPUT);
    pinMode(EN3, OUTPUT);
    pinMode(EN4, OUTPUT);
    pinMode(EN5, OUTPUT);
    pinMode(EN6, OUTPUT);
    Pin_Reset();
    Serial.begin(115200);
    Serial.println("Dieses Programm aktzeptiert über die serielle Schnittstelle bereitgestellte Bewegungsstrings zum lösen eines Zauberwürfels");
    Serial.println("Es steuert dafür sechs Schrittmotortreiber an");
    lastmovement = &movementList[0];
    amovement = &movementList[0];
}


void loop() {
  if ((Serial.available() > 0)) {        //Daten vorhanden
    Pin_Reset();
    Buffer = Serial.readString();               //einlesen
    Buffer.trim();                             //entfernt Steuerzeichen etc.
    amovement = lastmovement;
    lastmovement = cubeparser(lastmovement, Buffer);
   }
   while(amovement != lastmovement){
    switch (amovement->axes){
      case front : digitalWrite(EN1, LOW);
      break;
      case back : digitalWrite(EN2, LOW);
      break;
      case left : digitalWrite(EN3, LOW);
      break;
      case right : digitalWrite(EN4, LOW);
      break;
      case up : digitalWrite(EN5, LOW);
      break;
      case down : digitalWrite(EN6, LOW);
      break;
      case frontBack :  digitalWrite(EN1, LOW);
                        digitalWrite(EN2, LOW);
      break;
      case upDown : digitalWrite(EN3, LOW);
                    digitalWrite(EN4, LOW);
      break;
      case leftRight : digitalWrite(EN5, LOW);
                      digitalWrite(EN6, LOW);
      default : Pin_Reset();
    }
    if (amovement->direction == cw){
      digitalWrite(DIR, LOW);
    }
    else {
      digitalWrite(DIR, HIGH);
    }
    Fahren();
    delay(200);
    amovement++;
    Pin_Reset();
  }
}
