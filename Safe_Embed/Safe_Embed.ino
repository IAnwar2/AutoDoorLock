void setup() {
  Serial.begin(9600); // Set the baud rate to match the Python code
}

void loop() {
  // Do whatever you want with the received data
  if (Serial.available() > 0) {
    string data = Serial.read();

    // Process the received data
    Serial.print("Arduino received: ");
    Serial.println(data);

    if (data == "unlock"){
      Serial.println("Doors are unlocking");

    } else if (data == "lock"){
      Serial.println("Doors are locking");


    } 
  }
}
