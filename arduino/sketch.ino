#include <Servo.h>

#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 200

Servo RESC,LESC;     // create servo objects to control the ESC

int potValue;  // value from the analog pin

void setup() {
  // Attach the ESC on pin 9
  RESC.attach(9,1000,2000); // (pin, min pulse width, max pulse width in microseconds)
  LESC.attach(10,1000,2000); // (pin, min pulse width, max pulse width in microseconds)
  Serial.begin(9600);
}

void loop() {
   runBoat();
   delay(3000);
}

/////////////////tests////////////////////////////////////////
int potValForBLDC(){
  potValue = analogRead(A0);   // reads the value of the potentiometer (value between 0 and 1023)
  potValue = map(potValue, 0, 1023, 0, 180);   // scale it to use it with the servo library (value between 0 and 180)
  Serial.print("BLDC SPEED: ");
  Serial.println(potValue);
  return potValue;
}

int potValForStepper(){
  potValue = analogRead(A0);   // reads the value of the potentiometer (value between 0 and 1023)
  potValue = map(potValue, 0, 1023, 500, 5000);   // scale it to use it with the servo library (value between 500 and 5000)
  Serial.print("Stepper SPEED: ");
  Serial.println(potValue);
  return potValue;
}

void testRight(){
   int speed = potValForBLDC();
   RESC.write(speed);
}

void testLeft(){
   int speed = potValForBLDC();
   LESC.write(speed);
}

void testShredderForwarrd(){
   int speed = potValForStepper();
   digitalWrite(dirPin, HIGH);
   for (int i = 0; i < 10 * stepsPerRevolution; i++) {
      // These four lines result in 1 step:
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(speed);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(speed);
   }
}

void testShredderBackwarrd(){
   int speed = potValForStepper();
   digitalWrite(dirPin, LOW);
   for (int i = 0; i < 10 * stepsPerRevolution; i++) {
      // These four lines result in 1 step:
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(speed);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(speed);
   }
}
/////////////////tests////////////////////////////////////////

////////////////Functions/////////////////////////////////////

void runForward(int speed){
   RESC.write(speed);
   LESC.write(speed);
}

void turnLeft(int speed){
   RESC.write(2*speed);
   LESC.write(speed);
}

void turnRight(int speed) {
   RESC.write(speed);
   LESC.write(2*speed);
}

void shred(boolean isForward, int revs, int speed){
   digitalWrite(dirPin, isForward);
   for (int i = 0; i < revs * stepsPerRevolution; i++) {
      // These four lines result in 1 step:
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(speed);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(speed);
   }
}

void idle(){
   RESC.write(0);
   LESC.write(0);
   digitalWrite(stepPin, LOW);
   digitalWrite(dirPin, LOW);
}

int serialSignal(){
   while(!Serial.available())
      ;
   int signal = Serial.readString().toInt();
   return signal;
}

void runBoat(){
   int cs = serialSignal();

   switch (cs){
      case 0:
         Serial.println("Running forward...");
         runForward(20);
         break;
      
      case 1:
         Serial.println("Turning right...");
         turnRight(10);
         break;

      case 2:
         Serial.println("Turning left...");
         turnLeft(10);
         break;

      case 3:
         Serial.println("Shredding...");
         shred(true,10,1000);
         break;
      
      default:
         Serial.println("Idle...");
         idle();
         break;
   }
}

////////////////Functions/////////////////////////////////////