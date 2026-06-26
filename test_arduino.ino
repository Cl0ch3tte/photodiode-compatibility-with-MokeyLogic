void setup() {

  Serial.begin(115200);
  pinMode(7, INPUT);
}

void loop() {

  int etat = digitalRead(7);
  unsigned long t = micros();
  Serial.print(t);
  Serial.print(","); 
  Serial.println(etat); 
}