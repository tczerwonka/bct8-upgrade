#!/usr/bin/python


#read test

import sys
import time
import os
import serial

#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print(ser.name)
while True:
   data = ser.readline()[:-2] #get rid of newline cr
   if data:
      print data

