#!/usr/bin/python


#read test

import sys
import time
import os
import serial

#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
while True:
   data = ser.readline()[:-2] #get rid of newline cr
   if data:
      print data
   if (data == "y"):
      ser.write("192\r\n")
      time.sleep(1)
      ser.write("168\r\n")
      time.sleep(1)
      ser.write("001\r\n")
      time.sleep(1)
      ser.write("068\r\n")



