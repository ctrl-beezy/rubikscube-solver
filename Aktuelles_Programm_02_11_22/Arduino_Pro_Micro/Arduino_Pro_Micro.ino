#include <Wire.h>
#include <String.h>

String Buffer;                                    //String erstellen, um serielle Daten Zwischenzuspeichern
int Rotationen = 0;
bool busy = false;
int Zeit = 60;
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
}


void loop() {
  if ((Serial.available() > 0)&&(!busy))        //Daten vorhanden
  { 
    Pin_Reset();
    busy = true;             
    Buffer = Serial.readString();               //einlesen
    Buffer.trim();                              //entfernt Steuerzeichen etc.
    Serial.println(Buffer);
    Rotationen = 1;                             //default Wert
    switch (Buffer[0]) {                        //??? ansteuern
      case 'F': digitalWrite(EN1, LOW);
      break;
      case 'R': digitalWrite(EN2, LOW);
      break;
      case 'B': digitalWrite(EN3, LOW);
      break;
      case 'U': digitalWrite(EN4, LOW);
      break;
      case 'L': digitalWrite(EN5, LOW);
      break;
      case 'D': digitalWrite(EN6, LOW);
      break;         
    }
    
    if(Buffer.length() == 1) {                     //vor
        Schritt_vor();
    }   
    
    if (Buffer.length() == 3){                     //anzahl von zurück
      Rotationen = Buffer[2]-'0';
    }
    
    if(Buffer.length() >= 2) {
      if(Buffer[1] == 0x27) {                      //zurück      
        Schritt_rueck();
      }
      else if(Buffer[1]> '0' && Buffer[1]<='2') {  //vor mit anzahl
        Rotationen = Buffer[1]-'0';
        Schritt_vor();
      }
    }
    Pin_Reset();
    busy = false;
   }
}
