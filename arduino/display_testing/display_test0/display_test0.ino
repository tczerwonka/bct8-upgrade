
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
#include <Keypad.h>

// Pin definitions
byte N_SCK = 3;
byte SI = 4;
byte CD = 5;
byte RESET = 6;
byte BUSY = 7;
byte CS = 8;

// Initialize the library with the interface pins
KTMS1201 lcd(N_SCK, SI, CD, RESET, BUSY, CS);

//keypad stuff
/*
const byte ROWS = 5;
const byte COLS = 5;
char keys[ROWS][COLS] = {
  {'1','2','3','A','B'},
  {'4','5','6','B','C'},
  {'7','8','9','D','F'},
  {'.','0','E','G','H'},
  {'I','J','K','L','M'}
};
byte rowPins[ROWS] = {11, 12, 13, 14, 15};
byte colPins[COLS] = {2, 9, 10, 16, 17};
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
*/

const byte ROWS = 3;
const byte COLS = 1;
char keys[ROWS][COLS] = {
  {'a'},
  {'b'},
  {'c'}
};
byte rowPins[ROWS]={12,13,14};
byte colPins[COLS]={9};
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );






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

  
  char key = keypad.getKey();

  if (key != NO_KEY) 
  {
    Serial.println(key);
  }

  
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
  */
  /*
  lcd.specialChar("HWY");
  delay(1000);
  lcd.specialChar("SRH");
  delay(1000);
  lcd.specialChar("HLD");
  delay(1000);
  lcd.specialChar("P");
  delay(1000);
  lcd.specialChar("DN");
  delay(1000);
  lcd.specialChar("PRI");
  delay(1000);
  lcd.specialChar("DEC");
  delay(1000);
  lcd.specialChar("LO");
    delay(1000);
  lcd.specialChar("DLY");
  delay(1000);
  lcd.specialChar("DTA");
  delay(1000);
  lcd.specialChar("FLS");
  delay(5000);
*/



  //Set the cursor at the 9th digit
  lcd.setCursor(8);

  // Print seconds
  lcd.print(millis()/1000);
}
