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


