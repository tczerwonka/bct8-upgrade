#!/usr/bin/python

# start of client to communicate between front panel arduino over
# serial and the udp enabled rtl_fm

# start rtl_fm thusly:
# rtl_udp -l 120 -f 154.725M -s 200000 -r 48000 | aplay -r 48000 -f S16_LE -c 1
# -q -V mono -D sysdefault:CARD=ALSA


#read test

import socket, sys
import time
import os
import serial
import re


#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
frequency = 146520000


################################################################################
# need WBFM vs NBFM in udp_client
# need startups for rtl_udp and this client
# need frequency min and max limits
# need scanning functionality
# need to modify arduino code to blank leading zero in frequency
################################################################################



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
                #print mhz + "." + ltmhz
                print candidate_frequency
                ser.write("#" + mhz + "." + ltmhz + "\r\n")
                #this seems OK but arduino has problems with leading zero?
            if (data == "E"):
                # user says this is a frequency
                frequency = int(candidate_frequency)
                print "frequency is:"
                print frequency
                if frequency < 100000:
                    frequency = frequency * 1000
                    print "lt"
                else: 
                    frequency = frequency * 100
                    print "gt"
                candidate_frequency = "00000000"
                #udp call
                udp_send("freq", frequency)
            if (data == "M"):
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
# udp_send -- almost an exact topy of udpclient.py
################################################################################
def udp_send(mode, data):
    #open network
    print "programming:"
    print data
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("localhost", 6020))
    buf = ""
    if mode == 'freq':
        buf = buf + chr(0)
        print "sending freq"
        print data
        print "--"

    data = int(data)
    i=0
    while i < 4:
        buf = buf + chr(data & 0xff)
        data = data >> 8
        i = i + 1

    s.send(buf)
    s.close()
    return

    

################################################################################
# scanner class
################################################################################
class Scanner:
    frequency = 146520000

    def __init__(self, name):
        self.name = name



################################################################################
if __name__ == "__main__":
    main()
