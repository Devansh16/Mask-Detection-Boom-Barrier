#include <Servo.h>

Servo myservo;  

int data;
int LED=13;

void setup() 
{   
  Serial.begin(9600);                               
  pinMode(LED, OUTPUT);                    
  digitalWrite (LED, LOW);                     
  
  myservo.attach(9);  
  myservo.write(0);
}

void loop() 
{
  while (Serial.available())    
  { 
    data = Serial.read();
  }
  
  if (data == '1')
  {
    digitalWrite (LED, HIGH);
    myservo.write(90);             
    delay(5000);
    myservo.write(0);              
  }                 
  else if (data == '0')
  {
  digitalWrite (LED, LOW);                  
  myservo.write(0);
  }
}
