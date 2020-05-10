
/*
  ##############################################################################
  # arduino display client
  #
  # uses the KTMS1201 library
  # Developed and maintanied by MCUdude
  # https://github.com/MCUdude/KTMS1201
  ##############################################################################
*/

#include "BCT8-PD7225.h"
#include <Keypad.h>
#include "pindefs.h"

const byte numChars = 16;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;
int dataNumber = 0;             // new for this version
static float version = 100.0002;


void setup() {
  Serial.begin(9600);
  lcd.begin();
  lcd.clear();            // Clear the entire LCD
  pinMode(13, OUTPUT);    // this is the ALERT red light
  pinMode(19, INPUT);     // this is the alert pushbutton
  pinMode(20, INPUT);     // this is the flash pushbutton
  Serial.println("DISPLAYUP");
  //print version
  lcd.clear();
  lcd.setCursor(5);
  lcd.print(version,4);
  lcd.specialChar("FLS");
  delay(1000);
  lcd.clear();
}



/////////////////////////////////////////////////////////////////////////////
// loop
/////////////////////////////////////////////////////////////////////////////
void loop() {
  // check for pending event
  char key = keypad.getKey();

  if (key != NO_KEY) {
    Serial.println(key);
  }

  recvWithEndMarker();
  showNewNumber();


}



/////////////////////////////////////////////////////////////////////////////
// recvWithEndMarker()
/////////////////////////////////////////////////////////////////////////////
void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  if (Serial.available() > 0) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}



/////////////////////////////////////////////////////////////////////////////
// recvWithEndMarker()
/////////////////////////////////////////////////////////////////////////////
void showNewNumber() {
  if (newData == true) { 
    bool unprocessed = true;

    //if the string starts with a ! it's a special char
    if (receivedChars[0] == '!' && unprocessed) {
      char* specChar = &receivedChars[1];
      lcd.specialChar(specChar);
      unprocessed = false;
    }
    
    //prefix numbers with #
    if (receivedChars[0] == '#' && unprocessed) {
      String freq = &receivedChars[1];
      float f_freq = freq.toFloat();
      lcd.setCursor(5);
      lcd.print(f_freq,4);
      //Serial.println(f_freq,4);
      unprocessed = false;
    }

    //clear screen
    if (receivedChars[0] == '@' && unprocessed) {
      lcd.clear();
      unprocessed = false;
    }

    //print three chars
    if (unprocessed) {
      lcd.alphaNumeric(receivedChars);
    }

    newData = false;
  }
}
