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
  for (int j=0; j<Rotationen; j++){ 
    for(int i=0; i<(3300); i++){
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

void leseSchritt(String string){
  Rotationen = 1;                             //default Wert   
  //digitalWrite(EN1, LOW);
  switch (string[0]) {                        //??? ansteuern
    case 'F': digitalWrite(EN2, LOW);
    break;
    case 'R': digitalWrite(EN6, LOW);
    break;
    case 'B': digitalWrite(EN5, LOW);
    break;
    case 'U': digitalWrite(EN1, LOW);
    break;
    case 'L': digitalWrite(EN4, LOW);
    break;
    case 'D': digitalWrite(EN3, LOW);
    break;         
    }
      
      if(string.length() == 1) {                     //vor
          Schritt_vor();
      }   
      
      if (string.length() == 3){                     //anzahl von zurück
        Rotationen = string[2]-'0';
      }
      
      if(string.length() >= 2) {
        if(string[1] == 0x27) {                      //zurück      
          Schritt_rueck();
        }
        else if(string[1]> '0' && string[1]<='2') {  //vor mit anzahl
          Rotationen = string[1]-'0';
          Schritt_vor();
        }
      }
}
