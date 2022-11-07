#include "stepContr.hpp"
#include <Wire.h>

#define DIR 10
#define STEP 16
#define EN1 2
#define EN2 3
#define EN3 4
#define EN4 5
#define EN5 6
#define EN6 7

String Buffer;                                    //String erstellen, um serielle Daten Zwischenzuspeichern
int Rotationen = 0;
bool busy = false;
int Zeit = 100;
int cnt1 = 0;
int Drehungen = 0;


void Pin_Reset(){
  digitalWrite(EN1, HIGH);
  digitalWrite(EN2, HIGH);
  digitalWrite(EN3, HIGH);
  digitalWrite(EN4, HIGH);
  digitalWrite(EN5, HIGH);
  digitalWrite(EN6, HIGH);
}

void Schritt(int Zeit){
   digitalWrite(STEP, HIGH);
   delayMicroseconds(Zeit);
   digitalWrite(STEP, LOW);
   delayMicroseconds(Zeit);
}

void Fahren(){
   for(int i=0; i<Rotationen; i++){
      for(int i=0; i<410; i++){
        Schritt(Zeit);
      }
}
}

void Schritt_vor() {
    digitalWrite(DIR, LOW);
    Fahren();
}

void Schritt_rueck() {
    digitalWrite(DIR, HIGH);
    Fahren();
}

void leseSchritt(String movestring){
  Rotationen = 1;                             //default Wert   
  //digitalWrite(EN1, LOW);
  switch (movestring[0]) {                        //??? ansteuern
    case 'F': digitalWrite(EN6, LOW);
    break;
    case 'R': digitalWrite(EN4, LOW);
    break;
    case 'B': digitalWrite(EN1, LOW);
    break;
    case 'U': digitalWrite(EN2, LOW);
    break;
    case 'L': digitalWrite(EN5, LOW);
    break;
    case 'D': digitalWrite(EN3, LOW);
    break;         
    }
      
      if(movestring.length() == 1) {                     //vor
          Schritt_vor();
      }   
      
      if (movestring.length() == 3){                     //anzahl von zurück
        Rotationen = movestring[2]-'0';
      }
      
      if(movestring.length() >= 2) {
        if(movestring[1] == 0x27) {                      //zurück      
          Schritt_rueck();
        }
        else if(movestring[1]> '0' && movestring[1]<='2') {  //vor mit anzahl
          Rotationen = movestring[1]-'0';
          Schritt_vor();
        }
      }
}
