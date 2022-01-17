#!/usr/bin/python
################################################################################
#second version of the scanner client supporting P25
#
#TRUNK key sets to local P25 public safety
#DATA key shows IP address
#SRCH turns on NRSC5 decode
#MUTE does a shutdown
#
#receives output from modified op25 code via mqtt
#other side is
#mosquitto_sub -h localhost -t 'mqtt/p25'
#test with
#mosquitto_pub -h localhost -t 'mqtt/p25' -m "01/15/22 18:47:02.949287 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde"
#
#added this to crontab
#@reboot /usr/bin/screen -d -m -S fpclient /home/timc/bct8-upgrade/pi/bin/scan_client1.py
################################################################################
#pip install paho-mqtt
################################################################################


import socket, sys
import time
import os
import signal
import serial
import re
import subprocess
import shlex

#mqtt stuff
import paho.mqtt.client as mqttClient
Connected = False
broker = "localhost"

hd_audio_channel = -1
PID = 0

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
                #shutdown
                time.sleep(1)
                ser.write("OFF\r\n")
                time.sleep(1)
                os.system("/sbin/poweroff")
            if (data == "M"):
                ser.write("!HAM\r\n")
            if (data == "k"):
                ser.write("!MRN\r\n")
                trunk1()
            if (data == "U"):
                ser.write("146\r\n")
            if (data == "D"):
                ser.write("#146.520\r\n")
            if (data == "r"):
                nrsc5()
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
    mqtt_init()
    read_loop()
     


################################################################################
# setup
################################################################################
def setup():
    ser.write("@\r\n")



################################################################################
#mqtt init
################################################################################
def mqtt_init():
    client = mqttClient.Client("Python")
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port=1883)
    client.loop_start()
    while Connected != True:
        print "not connected"
        time.sleep(0.1)
    print client.subscribe('mqtt/p25')



################################################################################
# nrsc5
# HD audio
# this doesn't die - need to do better with process crap
################################################################################
def nrsc5():
    global hd_audio_channel
    global PID
    hd_audio_channel = hd_audio_channel + 1
    if (hd_audio_channel == 3): 
        hd_audio_channel = 0
    ch = str(hd_audio_channel)
    ser.write("HD" + ch + "\r\n")
    print "hda " + ch
    if (PID):
        os.kill(PID, signal.SIGTERM)
    PID = subprocess.Popen(['/usr/local/bin/nrsc5', '88.7', ch])



################################################################################
# trunk1
# start the trunking process via shell script
################################################################################
def trunk1():
    global PID
    time.sleep(1)
    ser.write("#152.7250\r\n")
    time.sleep(1)
    ser.write("!WX\r\n")
    if (PID):
        os.kill(PID, signal.SIGTERM)
    PID = subprocess.Popen('/home/timc/op25.sh')



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

    #if this is the local sheriff
    if re.match(r".+NAC 0x230", message.payload):
        #print message.payload.split("=")
        r = message.payload.split("=")
        show_last_call(r[5][2:])



################################################################################
#show_last_call
#this should be a file someday
#1 - 49 County Sheriff's Office
#'2318c9': -- 27
#50 - 51 County Emergency Management
#70 - 79 Monticello Police Department
#'2333cd' -- 77 monticello
#80 - 89 New Glarus Police Department
#90 - 95 Brooklyn Police Department
#96 - 99 County Coroner's Office
#100 - 199 Brodhead Police Department
#200 - 299 Monroe Police Department
#300 - 324 County Sheriff's Office (Part-Time Employees)
#325 - 326 County Humane Society
#400 - 499 Albany Police Department
#720 - 729 Brodhead Fire Department
#740 - 749 Juda Community Fire Department
#750 - 759 Monroe Fire Department (Apparatus)
#800 - 899 County EMS Units
#6100 - 6199 Belleville Police Department
#7500 - 7599 Monroe Fire Department (Personnel)
#       '326a41': 'BLN', -- blanchardville
#################################################################################
def show_last_call(radio_id):
    radio_id = radio_id.strip()
    dict = {
        '000001': 'UNK',
        '0059da': 'DSP', 
        '0059db': 'DSP', 
        '0059dc': 'DSP', 
        '0059d9': 'DSP', 
        '2318c7': 'S10',
        '2318c9': 'S27',
        '2318ca': 'S17',
        '2318d1': 'S04',
        '2318d2': 'S05',
        '2318d9': 'S31',
        '23ce06': 'NG2',
        '23ce08': 'NG1',
        '23cc14': 'NG4',
        '23ce07': 'NG4',
        '2333bd': 'MON',
        '2333cc': 'MCL',
        '2333cd': 'MCL',
        '233fde': 'foo',
        '326a41': 'BLN',
        '16777215': 'ALB'
    }
    if dict.get(radio_id):
        print "heard: " + radio_id + ": " + dict.get(radio_id)
        ser.write(dict.get(radio_id) + "\r\n")
    else:
        print "unknown RID:" + radio_id + ":"
        ser.write("UNK\r\n")

    


################################################################################
#mqtt on_connect
################################################################################
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







