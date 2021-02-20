 #include <Stepper.h>

 #include <stdio.h>

 #include <string.h>

 #include <stdlib.h>

 // Function to concatenate 
 // two integers into one 
 int concat(int a, int b) {
   if (a == 0) {
     return (b);
   }
   char s1[20];
   char s2[20];

   // Convert both the integers to string 
   sprintf(s1, "%d", a);
   sprintf(s2, "%d", b);

   // Concatenate both strings 
   strcat(s1, s2);

   // Convert the concatenated string 
   // to integer 
   int c = atoi(s1);

   // return the formed integer 
   return c;
 }
 
 #define STEPS 2038 // the number of steps in one revolution of your motor (28BYJ-48)

 Stepper stepper(STEPS, 8, 10, 9, 11);
 int arr[] = {  //this array can take in a maximum of 6 integers from serial input 
   0,
   0,
   0,
   0,
   0,
   0
 };
 unsigned int arr_length = 0;
 int incomingByte = 0; // for incoming serial data
 void setup() {
   Serial.begin(9600); // initialize the serial communication
   // Note: analog pins are automatically set as inputs
 }

 void loop() {

   if (Serial.available() > 0) {

     // read the incoming byte:
     incomingByte = Serial.read();
     arr[arr_length] = incomingByte;
     arr_length = arr_length + 1;
     Serial.print("incoming byte: ");
     Serial.println(incomingByte); // print out the value you read

     bool negative = false; // negative steps flag
    
     if (incomingByte == 4) { // 4 in assci indicates end of tranmission
       Serial.println("eot");
       int steps = 0;
       boolean printanologvalue=true;
       for (int i = 0; i < arr_length - 1; i++) { //loop through the array containing the bytes
         
         if (arr[i] == 45) {   // negative steps
           negative = true;
         }
         else if (arr[i] == 110){
          printanologvalue= false;
          }
         else {
           Serial.print("num: ");
           Serial.println(arr[i] - 48);
           steps = concat(steps, arr[i] - 48); //concatnates 
         }

       }
       
       if (negative == true) {
         steps = -steps;
       }
       Serial.print("total steps: ");
       Serial.println(steps);
       stepper.setSpeed(10); // 16 rpm //my motor can do 16rpm reliably
       stepper.step(steps); // do x steps 
       memset(arr, 0, sizeof(arr)); //resets the array to zeros
       arr_length = 0; 
       int potValue=0;
       if (printanologvalue==true){


        for (int i = 0; i < 5; i++) {
       potValue = analogRead(A2) + potValue; // get a reading from the potentiometer on A2
        }
       
       delay(100);
     }
     potValue=potValue/5;
       Serial.println((String)"potentiometer average value (5 readings) = "+potValue ); // print out the value you read
       Serial.println("DONE");
       Serial.flush();
     }

   } 
   
   
   else {
//     Serial.println("nothing in serial");
//     for (int i = 0; i < 6 - 1; i++) {
//       Serial.print("arr value: ");
//       Serial.println(arr[i]);
//     }
     //delay(100);
   }

 }