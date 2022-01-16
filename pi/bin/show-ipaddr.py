#!/usr/bin/python

################################################################################

#read test


import sys
import time
import os
import serial
import socket



#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
while True:
   data = ser.readline()[:-2] #get rid of newline cr
   if data:
      print data
   if (data == "d"):
      #depends on route out but whatever
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      octets = s.getsockname()[0].split('.')
      ser.write('@\r\n')
      ser.write(octets[0].ljust(3))
      ser.write('\r\n')
      time.sleep(1)
      ser.write(octets[1].ljust(3))
      ser.write('\r\n')
      time.sleep(1)
      ser.write(octets[2].ljust(3))
      ser.write('\r\n')
      time.sleep(1)
      ser.write(octets[3].ljust(3))
      ser.write('\r\n')
      time.sleep(1)
      ser.write('@\r\n')



