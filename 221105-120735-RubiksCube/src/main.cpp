#include "motorContr.hpp"
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
}


void loop() {
  if ((Serial.available() > 0)&&(!busy))        //Daten vorhanden
  { 
    Pin_Reset();
    busy = true;             
    Buffer = Serial.readString();               //einlesen
    Buffer.trim();                              //entfernt Steuerzeichen etc.

    String substring;
    do{
    substring = Buffer.substring(index, Buffer.indexOf(' ', index));
    Serial.println(substring);
    leseSchritt(substring);
    delay(400);
    Pin_Reset();
    index = Buffer.indexOf(' ', index)+1;
    } while((index-1) != -1);
    busy = false;
   }
}
