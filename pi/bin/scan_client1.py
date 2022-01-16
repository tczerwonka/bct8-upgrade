#!/usr/bin/python
################################################################################
#second version of the scanner client supporting P25
#
#TRUNK key sets to local P25 public safety
#
#receives output from modified op25 code via mqtt
#other side is
#mosquitto_sub -h localhost -t 'mqtt/p25'
#test with
#mosquitto_pub -h localhost -t 'mqtt/p25' -m "01/15/22 18:47:02.949287 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde"
################################################################################
#pip install paho-mqtt
################################################################################


import socket, sys
import time
import os
import serial
import re
import subprocess
import shlex

#mqtt stuff
import paho.mqtt.client as mqttClient
Connected = False
broker = "localhost"


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
                time.sleep(1)
                ser.write("@\r\n")
                print "clear"
            if (data == "M"):
                ser.write("!HAM\r\n")
            if (data == "k"):
                ser.write("!MRN\r\n")
                trunk1()
            if (data == "U"):
                ser.write("146\r\n")
            if (data == "D"):
                ser.write("#146.520\r\n")
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
# trunk1
# start the trunking process
################################################################################
def trunk1():
    time.sleep(1)
    ser.write("#152.7250\r\n")
    time.sleep(1)
    ser.write("!WX\r\n")
    time.sleep(1)

    client = mqttClient.Client("Python")
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port=1883)
    client.loop_start()
    while Connected != True:
        print "not connected"
        time.sleep(0.1)
    print client.subscribe('mqtt/p25')
    s = subprocess.Popen('/home/timc/op25.sh')



################################################################################
#mqtt stuff
#to test without traffic
#mosquitto_pub -h localhost -t 'mqtt/p25' -m "01/15/22 18:47:02.949287 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde"
################################################################################
def on_message(client, userdata, message):
    #print "Message received: "  + message.payload
    #somewhere in here parse the strings from op25
    #print type(message.payload)
    #01/15/22 18:47:02.949287 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde 
    #01/15/22 18:47:03.313039 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde 
    #01/15/22 18:47:03.373206 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=15, src_addr=0x233fde 
    #01/15/22 18:47:04.207448 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x0059db 
    #characters = [chr(ascii) for ascii in message.payload] #convert ascii to char
    #char_join = ''.join(characters)
    if re.match(r".+NAC", message.payload):
        print message.payload.split("=")
        r = message.payload.split("=")
        print r[5]
        ser.write("fde\r\n")



def on_connect(client, userdata, frlags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")


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






