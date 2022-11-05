#include <Wire.h>
#include <string.h>

volatile String Buffer;                                    //String erstellen, um serielle Daten Zwischenzuspeichern
int Rotationen = 0;
bool busy = false;
int Zeit = 220;
int cnt1 = 0;
int Drehungen = 0;

#define DIR 10
#define STEP 16
#define EN1 2
#define EN2 3
#define EN3 4
#define EN4 5
#define EN5 6
#define EN6 7

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
}


void loop() {
  if ((Serial.available() > 0)&&(!busy))        //Daten vorhanden
  { 
    Pin_Reset();
    busy = true;             
    Buffer = Serial.readString();               //einlesen
    Buffer.trim();                              //entfernt Steuerzeichen etc.
    int index = 0;
    String substring;
    do{
    substring = Buffer.substring(index, Buffer.indexOf(' ', index));
    Serial.println(substring);
    leseSchritt(substring);
    delay(200);
    Pin_Reset();
    index = Buffer.indexOf(' ', index)+1;
    } while((index-1) != -1);
    busy = false;
   }
}
