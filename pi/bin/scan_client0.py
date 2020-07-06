#!/usr/bin/python

# start of client to communicate between front panel arduino over
# serial and the udp enabled rtl_fm

#read test

import sys
import time
import os
import serial
import re

#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
frequency = 146520000

################################################################################
################################################################################
def read_loop():
    #open serial port
    state = 0
    candidate_frequency = "00000000"
    while True:
        data = ser.readline()[:-2] # get rid of newline cr
        if data:
            print data
            #check if a number -- if so this is a frequency
            if re.match(r"[0-9]", data):
                state = 1
                print "number"
                candidate_frequency+=str(data)
                candidate_frequency = candidate_frequency[-7:]
                mhz = candidate_frequency[:3]
                ltmhz = candidate_frequency[-4:]
                print mhz + "." + ltmhz
                print candidate_frequency
                ser.write("#" + mhz + "." + ltmhz + "\r\n")
                #this seems OK but arduino has problems with leading zero?
            if (data == "E"):
                ser.write("@\r\n")
                print "clear"
            if (data == "M"):
                ser.write("!HAM\r\n")
            if (data == "U"):
                ser.write("146\r\n")
            if (data == "D"):
                ser.write("#146.520\r\n")


################################################################################
# main
################################################################################
def main():
    setup()
    read_loop()
     


################################################################################
# setup
################################################################################
def setup():
    ser.write("@\r\n")


################################################################################
if __name__ == "__main__":
    main()



################################################################################
# scanner class
################################################################################
class Scanner:
    frequency = 146520000

    def __init__(self, name):
        self.name = name

