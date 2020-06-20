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
    Serial.println(data);
  }
  
  if (data == 'o')
  {
    digitalWrite (LED, HIGH);
    myservo.write(90);             
    delay(5000);
    myservo.write(0);              
  }                 
  else if (data == 'c')
  {
  digitalWrite (LED, LOW);                  
  myservo.write(0);
  }
}
