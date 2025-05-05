#include <Servo.h>  // Library untuk servo

// Pin untuk Motor DC
#define DIR_A D1
#define PWM_A D3
#define DIR_B D2
#define PWM_B D4

// Pin untuk Servo
#define SERVO_PIN D5  // Pin untuk servo 

// Inisialisasi objek servo
Servo myServo;

// Pin untuk Sensor Garis
// #define S1 D4  // Sensor 1
// #define S2 D5  // Sensor 2 
// #define S3 D6  // Sensor 3 
// #define S4 D7  // Sensor 4 
// #define S5 D8  // Sensor 5 

String buff, buff_motor, buff_servo;
const char delimiter[] = ":";  // The delimiter
int motor, servo;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
//  Serial2.begin(115200);
//  Serial2.println("Program Dimulai");

  pinMode(DIR_A, OUTPUT);
  pinMode(PWM_A, OUTPUT);
  pinMode(DIR_B, OUTPUT);
  pinMode(PWM_B, OUTPUT);
  myServo.attach(SERVO_PIN);
  stopMotor(0);
  myServo.write(0);
//  Serial2.println("Servo di posisi awal (0 derajat)");

  // pinMode(S1, INPUT);
  // pinMode(S2, INPUT);
  // pinMode(S3, INPUT);
  // pinMode(S4, INPUT);
  // pinMode(S5, INPUT);
}

void loop() {
   // put your main code here, to run repeatedly:
   if (Serial.available() > 0) {
    
    // read the oldest byte in the serial buffer:
    buff = Serial.readString();// read the incoming data as string
//    Serial1.println(buff);  //debugging purpose
    
    if (buff[0] == 'M'){
      buff_motor=buff;

      // Convert String to a mutable character array
      char buff_motor_array[buff_motor.length() + 1]; // Create a buffer
      buff_motor.toCharArray(buff_motor_array, sizeof(buff_motor_array)); // Convert String to char array

      // Use strtok() to split
    char *token = strtok(buff_motor_array, delimiter);
    if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
            motor = atoi(token);  // Convert second token to integer
        }
    }
    forward(motor);
    delay(1000);
    }
    
    else if (buff[0] == 'A'){
      buff_servo=buff;
      
      // Convert String to a mutable character array
      char buff_servo_array[buff_servo.length() + 1]; // Create a buffer
      buff_servo.toCharArray(buff_servo_array, sizeof(buff_servo_array)); // Convert String to char array

      // Use strtok() to split
    char *token = strtok(buff_servo_array, delimiter);
    if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
            servo = atoi(token);  // Convert second token to integer
        }
    }
    myServo.write(servo);

    }
  }
  
}

void forward(int num) {
  digitalWrite(DIR_A, HIGH);
  digitalWrite(DIR_B, HIGH);
  analogWrite(PWM_A, num);
  analogWrite(PWM_B, num);
}

void reverse(int num){
  digitalWrite(DIR_A, LOW);
  digitalWrite(DIR_B, LOW);
  analogWrite(PWM_A, num);
  analogWrite(PWM_B, num);
}

void stopMotor(int num) {
  analogWrite(PWM_A, num);
  analogWrite(PWM_B, num);
}
