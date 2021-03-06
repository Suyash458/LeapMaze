#include<Servo.h>

Servo MyServo1,MyServo2;
char input1,input2,input3;
int count = 0;
const int buttonPin = 8;  

//Inner servo : 50 (MyServo2)
//Outer Servo : 35 (MyServo1)
void setup()
{
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  MyServo1.attach(11);    
  MyServo2.attach(10);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
//MyServo.writeMicroseconds(500);
  MyServo1.write(45);
  MyServo2.write(95);
  delay(500);
 // MyServo1.detach();
//  MyServo2.detach();
}

void loop()
{  
  
  int buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {     
    // turn LED on:    
  MyServo1.write(45);
  MyServo2.write(95);
  //MyServo2.detach();
  } 
  else 
  {
  MyServo1.attach(11);
  MyServo2.attach(10);    
  while(Serial.available()>2)
  {
    input1= Serial.read();
    if(input1 == 60)
    {
      input2 = Serial.read();  //Pitch
      input3 = Serial.read();  //Roll
      //MyServo.write(500 + (2./5*(input/2.8)));
      if(!(((45 + input2/5) >= 75) || ((45 + input2/5 <=5))))
        MyServo1.write(45 + input2/5);
        delay(2);
      if(!(((95 + input3/5) >= 155) || ((95 + input3/5 <=75))))
        MyServo2.write(95 + input3/5);
        delay(2);
    }

  }
  }
}
