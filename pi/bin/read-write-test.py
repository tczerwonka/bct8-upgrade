#!/usr/bin/python


#read test

import sys
import time
import os
import serial

#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.write("@\r\n")
while True:
   data = ser.readline()[:-2] #get rid of newline cr
   if data:
      print data
      if (data == "E"):
          ser.write("@\r\n")
          print "clear"
      if (data == "M"):
          ser.write("!HAM\r\n")
      if (data == "U"):
          ser.write("146\r\n")
      if (data == "D"):
          ser.write("#146.520\r\n")

