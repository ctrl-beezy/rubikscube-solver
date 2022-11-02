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
      for(int i=0; i<200; i++){
        if(cnt1 < 20)
        {
          cnt1++;
          Schritt(Zeit);
        }
        else if(cnt1 = 20)
        {
          cnt1 = 0;
          Zeit--;
          Schritt(Zeit);
        }
      }
      for(int i=0; i<400; i++){
        Schritt(Zeit);
      }
      for(int i=0; i<200; i++){
        if(cnt1 < 20)
        {
          cnt1++;
          Schritt(Zeit);
        }
        else if(cnt1 = 20)
        {
          cnt1 = 0;
          Zeit++;
          Schritt(Zeit);
        }
      }
   Drehungen++;
   }
}

void Schritt_vor() {
    digitalWrite(DIR, HIGH);
    Fahren();
}

void Schritt_rueck() {
    digitalWrite(DIR, LOW);
    Fahren();
}
