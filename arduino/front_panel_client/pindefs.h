#ifndef DISPLAY_PINDEFS_H
#define DISPLAY_PINDEFS_H

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
const byte ROWS = 5;
const byte COLS = 5;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 's', 'y'},
  {'4', '5', '6', 'p', 'L'},
  {'7', '8', '9', 'v', 'd'},
  {'.', '0', 'E', 'r', 'p'},
  {'i', 'D', 'U', 'k', 'M'}
};
byte rowPins[ROWS] = {11, 12, 18, 14, 15};
byte colPins[COLS] = {2, 9, 10, 16, 17};
//swapped D2 for A4 -- 
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

#endif
