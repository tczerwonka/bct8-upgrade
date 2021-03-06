/*****************************************************************
  | KTM-S1201 Arduino library                                      |
  | Developed and maintanied by MCUdude                            |
  | https://github.com/MCUdude/KTMS1201                            |
  |                                                                |
  | Based on Tronixstruff's work                                   |
  | tronixstuff.com/2013/03/11/arduino-and-ktm-s1201-lcd-modules   |
  | Released to the public domain                                  |
*****************************************************************/


#include "Arduino.h"

#ifndef KTMS1201_H
#define KTMS1201_H

//      ---   0x01
//0x10 |   |  0x02
//0x20  ---
//0x40 |   |  0x04
//0x80  --- o 0x08

/* LCD characters */
static const uint8_t numberOfCharacters = 67;
static const uint8_t sevenSegHex[67] = {0x06/*1*/, 0xE3/*2*/, 0xA7/*3*/, 0x36/*4*/, 0xB5/*5*/, 0xF4/*6*/, 0x07/*7*/, 0xF7/*8*/, 0x37/*9*/, 0xD7/*0*/, 0x00/*space*/, 0x20/*Dash*/, 0x80/*Underscore*/, 0x33/*Degree*/, 0xA0/*equal*/, 0x77/*A*/, 0xF4/*B*/, 0xE0/*C*/, 0xE6/*D*/, 0xF1/*E*/, 0x71/*F*/, 0xD5/*G*/, 0x74/*H*/, 0x04/*I*/, 0x86/*J*/, 0x70/*K*/, 0xD0/*L*/, 0x76/*M*/, 0x64/*N*/, 0xE4/*O*/, 0x73/*P*/, 0xDF/*Q*/, 0x60/*R*/, 0xB5/*S*/, 0xF0/*T*/, 0xC4/*U*/, 0xD6/*V*/, 0xF6/*W*/, 0x56/*X*/, 0xB6/*Y*/, 0xEB/*Z*/, 0x77/*a*/, 0xF4/*b*/, 0xE0/*c*/, 0xE6/*d*/, 0xF1/*e*/, 0x71/*f*/, 0xD5/*g*/, 0x74/*h*/, 0x04/*i*/, 0x86/*j*/, 0x70/*k*/, 0xD0/*l*/, 0x76/*m*/, 0x64/*n*/, 0xE4/*o*/, 0x73/*p*/, 0xDF/*q*/, 0x60/*r*/, 0xB5/*s*/, 0xF0/*t*/, 0xC4/*u*/, 0xD6/*v*/, 0xF6/*w*/, 0x56/*x*/, 0xB6/*y*/, 0xEB/*z*/};
static const uint8_t charArray[67] = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ', '-', '_', '*', '=', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

/*------------------------------------*/
/* multi-segment chars */
struct multiSeg {
  char symbol;
  uint8_t sw;
  uint8_t ne;
};

static const uint8_t multiSegChars = 38;
static const multiSeg elementsAN[] = {
  {'A', B00100011, B01110100},
  {'B', B00100111, B00011010},
  {'C', B00000111, B00010000},
  {'D', B00100110, B01100100},
  {'E', B00100111, B00010000},
  {'F', B00100011, B00010000},
  {'G', B00000111, B01010100},
  {'H', B00100011, B01100100},
  {'I', B10000000, B00000001},
  {'J', B00000110, B01100000},
  {'K', B00100011, B00001010},
  {'L', B00000111, B00000000},
  {'M', B00010011, B01100010},
  {'N', B00010011, B01101000},
  {'O', B00000111, B01110000},
  {'P', B00100011, B00110100},
  {'Q', B00000111, B01111000},
  {'R', B00100011, B00111100},
  {'S', B00100101, B01010100},
  {'T', B10000000, B00010001},
  {'U', B00000111, B01100000},
  {'V', B00010000, B01101000},
  {'W', B01000011, B01101000},
  {'X', B01010000, B00001010},
  {'Y', B10010000, B00000010},
  {'Z', B01000100, B00010010},
  {'*', B11110000, B00001111},  
  {' ', B00000000, B00000000},
  {'0', B01000111, B01110010},
  {'1', B00000000, B01100000},
  {'2', B00100110, B00110100},
  {'3', B00000100, B01110100},
  {'4', B00100001, B01100100},
  {'5', B00100101, B01010100},
  {'6', B00100111, B01010100},
  {'7', B01000000, B00010010},
  {'8', B00100111, B01110100},  
  {'9', B00100101, B01110100}
};


/*------------------------------------*/
/* special characters */
struct specChar {
  char symbol[4];
  uint8_t pos;
  uint8_t code;
};


//these should probably be bit-wise OR'ed in
static const uint8_t specialCharacters = 34;
static const specChar elements[] = {
  {"MRN", 0, B00000001},
  {"MLO", 0, B00000010},
  {"RMT", 0, B00000100},
  {"ATT", 0, B00001000},
  {"RR", 0, B00010000},
  {"AIR", 0, B00100000},
  {"CB", 0, B01000000},
  {"NWS", 0, B10000000},
  {"BN2", 1, B00000101},
  {"BN1", 1, B00000110},
  {"BNX", 1, B00001100},
  {"BN3", 1, B00010100},
  {"BN4", 1, B00100100},
  {"BN5", 1, B01000100},
  {"PVT", 2, B00000001},
  {"POL", 2, B00000010},
  {"WX", 2, B00000100},
  {"FIR", 2, B00001000},
  {"M", 2, B00010000},
  {"E", 2, B00100000},
  {"L", 2, B01000000},
  {"LST", 2, B10000000},
  {"TRK", 3, B00000001},
  {"HWY", 4, B00001000},
  {"SRH", 5, B10000000},
  {"HLD", 7, B10000000},
  {"P", 8, B00001000},
  {"DN", 9, B00001000},
  {"PRI", 10, B00001000},
  {"DEC", 11, B00001000},
  {"LO", 12, B00001000},
  {"DLY", 13, B00001000},
  {"DTA", 14, B00001000},
  {"FLS", 15, B00001000}

};

/*------------------------------------*/


/* LCD modes */
const uint8_t _Mode = 0x40;     // LCD speed. Se uPD7225 datasheet for more infp
const uint8_t _Sync = 0x31;     // Synchronized transfer
const uint8_t _USync = 0x30;    // Unsynchronized transfer
const uint8_t _FBlink = 0x1b;   // Blink fast (~2 Hz)
const uint8_t _SBlink = 0x1a;   // Blink slow (~1 Hz)
const uint8_t _NoBlink = 0x18;  // No blink
const uint8_t _DispOn = 0x11;   // Display on
const uint8_t _DispOff = 0x10;  // Display off
const uint8_t _Decode = 0x15;   // Turn on segment decoding
const uint8_t _NoDecode = 0x14; // Turn off segment decoding
const uint8_t _LoadPtr = 0xE0;  // Load data pointer
const uint8_t _SetDp = 0xb8;    // Set decimal point (Dp)
const uint8_t _ClearDp = 0x9f;  // Clear decimal point (Dp)
const uint8_t _ClearDsp = 0x20; // Clear display memory

const bool fast = true;
const bool slow = false;
const uint8_t busyDelay = 1;


class KTMS1201
{
  public:
    /* Public methods */
    KTMS1201(uint8_t NSCK, uint8_t SI, uint8_t CD, uint8_t RESET, uint8_t BUSY, uint8_t CS);
    KTMS1201(uint8_t NSCK, uint8_t SI, uint8_t CD, uint8_t RESET, uint8_t CS);

    void begin();
    void command(uint8_t);
    void customChar(uint8_t);
    void setCursor(uint8_t cursorPos = 0);
    void clear(uint8_t start = 0, uint8_t stop = 11);
    void blink(bool speed = slow);
    void noBlink();
    void display();
    void noDisplay();

    void print(String);
    void print(char*);
    void print(char);
    void print(uint32_t, uint8_t base = DEC);
    void print(int32_t, uint8_t base = DEC);
    void print(uint16_t, uint8_t base = DEC);
    void print(int16_t, uint8_t base = DEC);
    void print(double, uint8_t decimals = 2);

    void specialChar(String);
    void alphaNumeric(String);

  private:
    /* Private methods */
    void printNumber(uint32_t, uint8_t base = DEC, bool table = false);
    void printFloat(double, uint8_t = 2);
    void write(uint8_t);
    void wait();

    /* Private variables */
    uint8_t _cursorPos = 0;

    /* Digital pins */
    uint8_t _SCK = 0;
    uint8_t _SI = 0;
    uint8_t _CD = 0;
    uint8_t _RESET = 0;
    uint8_t _BUSY = 255;
    uint8_t _CS = 0;
};

#endif
