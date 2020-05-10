#!/usr/bin/python

## 22 November 2015
## T. Czerwonka tczerwonka@gmail.com
##

import sys
import time
import os
import platform 
import subprocess
import serial
from array import array
from socket import socket

WAITING = 0
READING = 1
DONE = 2
stream_state = WAITING


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003


sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)



#open serial port for reading
ser = serial.Serial('/dev/ttyACM0', 9600)
line = []
carbondata = []
#reset the arduino -- the internal program waits two seconds
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)

while stream_state != DONE:
	for c in ser.read():
		if stream_state == WAITING:
        		#found EOF character from previous burst -- all after this is valid
        		if c == '\x18': 
				stream_state = READING
				break

        	#found EOF character -- we're done now
		if stream_state == READING:
        		if c == '\x18':
				stream_state = DONE
				break
			#ignore newline and tab
			if c == "\r": break
			if c == "\t": break
			if c != "\n":
        			line.append(c)
        		if c == '\n':
            			#print(line)
  				now = int( time.time() )
				foo = array('B', map(ord,line)).tostring()
  				carbondata.append("%s %d" % (foo,now))
            			line = []
            		break

		#we're done here
		if stream_state == DONE:
			ser.close()
			break


message = '\n'.join(carbondata) + '\n' #all lines must end in a newline
#print "sending message\n"
#print message
sock.sendall(message)

sys.exit(0)

