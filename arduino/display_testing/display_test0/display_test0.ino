
/*
  ##############################################################################
  # arduino display test zero
  #
  # uses the KTMS1201 library
  # Developed and maintanied by MCUdude
  # https://github.com/MCUdude/KTMS1201
  ##############################################################################
*/

#include "BCT8-PD7225.h"

// Pin definitions
byte N_SCK = 3;
byte SI = 4;
byte CD = 5;
byte RESET = 6;
byte BUSY = 7;
byte CS = 8;

// Initialize the library with the interface pins
KTMS1201 lcd(N_SCK, SI, CD, RESET, BUSY, CS);

void setup()
{
  Serial.begin(9600);
  // Set up the LCD
  lcd.begin();
  // Set cursor at the first character
  //lcd.setCursor(0);

  lcd.clear();          // Clear the entire LCD
  //lcd.setCursor(1);     // Set cursor at index 0
  //lcd.customChar(0x08); // 0x40 + 0x20 + 0x02 = 0x62 -> slash
}

void loop()
{
  /*
    lcd.specialChar("MRN");
    delay(1000);
    lcd.specialChar("MLO");
    delay(1000);
    lcd.specialChar("RMT");
    delay(1000);
    lcd.specialChar("ATT");
    delay(1000);
    lcd.specialChar("RR");
    delay(1000);
    lcd.specialChar("AIR");
    delay(1000);
    lcd.specialChar("CB");
    delay(1000);
    lcd.specialChar("NWS");
    delay(1000);
  */
  lcd.specialChar("BN1");
  delay(1000);
  lcd.specialChar("BN2");
  delay(1000);
  lcd.specialChar("BN3");
  delay(1000);
  lcd.specialChar("BN4");
  delay(1000);
  lcd.specialChar("BN5");
  delay(1000);
  lcd.specialChar("PVT");
  delay(1000);    
  lcd.specialChar("POL");
  delay(1000);    
  lcd.specialChar("WX");
  delay(1000);    
  lcd.specialChar("FIR");
  delay(1000);    
  lcd.specialChar("M");
  delay(1000);
    lcd.specialChar("E");
  delay(1000);
    lcd.specialChar("L");
  delay(1000);
    lcd.specialChar("LST");
  delay(1000);
      lcd.specialChar("TRK");
  delay(5000);



  for (int i = 0; i <= 15; i++) {
    //lcd.setCursor(7);
    Serial.println(i);

    lcd.setCursor(i);
    lcd.customChar(0xff);
    delay(1000);


    /*
        for (int j = 0; j <= 15; j++) {
          lcd.setCursor(5);
          lcd.print(j);

          //print the element
          lcd.setCursor(i);
          lcd.customChar(j);
          delay(100);
        }
    */

    lcd.clear();
  }



  // Set the cursor at the 9th digit
  //lcd.setCursor(8);

  // Print seconds
  //lcd.print(millis()/1000);
}
