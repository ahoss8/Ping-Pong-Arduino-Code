const int swPin = 9;
const int xPin = A0;
const int yPin = A1;

int switchState;
int xDir;
int yDir;
int delayTime = 20;


void setup() {
  Serial.begin(115200);
  
  pinMode(swPin, INPUT);
  pinMode(xPin, INPUT); 
  pinMode(yPin, INPUT); 
  digitalWrite(swPin, HIGH); 

}


void loop() {
  switchState = digitalRead(swPin);
  xDir = analogRead(xPin);
  yDir = analogRead(yPin);

  Serial.print(switchState);
  Serial.print(", ");
  Serial.print(xDir);
  Serial.print(", ");
  Serial.println(yDir);
  delay(delayTime);

}
