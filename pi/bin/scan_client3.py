#!/usr/bin/python3

################################################################################
#scan_client3.py
#
# 2023 T Czerwonka tczerwonka@gmail.com
# Put a RPI and RTL-SDR plus an OLED into an old BCT8 scanner chassis
# along with an arduino to decode the front panel buttons
# 
################################################################################

import os
import socket, sys
from pathlib import Path
import datetime
import pytz
import time
import signal
import serial
import re
import subprocess
import shlex

################################################################################
#mqtt stuff
#receives output from modified op25 code via mqtt
#other side is
#mosquitto_sub -h localhost -t 'mqtt/p25'
#test with
#mosquitto_pub -h localhost -t 'mqtt/p25' -m "01/15/22 18:47:02.949287 [0] NAC 0x230 LCW: ec=0, pb=0, sf=0, lco=0, src_addr=0x233fde"
#pip install paho-mqtt
################################################################################
import paho.mqtt.client as mqttClient
Connected = False
broker = "localhost"

hd_audio_channel = -1

#open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

current_state = 'idle'
start_time = time.time()

#read the config file
import yaml


#oled
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, Image, ImageDraw    
from time import sleep

device=ssd1306(i2c(port=1, address=0x3C))
device.clear()

global UNIT
global UNIT1
global UNIT2
UNIT = 0
UNIT1 = 0
UNIT2 = 0

#uses PIL with image zones, hm.
### Initialize drawing zone (aka entire screen)
output = Image.new("1", (128,64))
add_to_image = ImageDraw.Draw(output)

################################################################################
#top line -- status -- rssi/time/mode
rssi_zone = [(0,10), (20, 20)]
rssi_start = (0,10)

time_zone = [(21,10), (100,20)]
time_start = (23,10)

mode_zone = [(101,10), (127,20)]
mode_start = (103,10)

freq_zone = [(0,21), (75,40)]
freq_start = (3,25)

label_zone = [(65,21), (127,40)]
label_start = (67,25)

text_zone = [(0,41), (127,63)]
text_start1 = (2,42)
text_start2 = (2,52)

#next line -- frequency
#next lines -- data -- 3 line buffer?
################################################################################

frequency = "select:"
mode = "P25"
start_time = time.time()

################################################################################
################################################################################

def mainloop(device):
    global frequency
    global mode
    global current_state
    global PID
    channel_struct = read_configfile('/home/timc/bct8-upgrade/misc/scannerlist.yaml')
    total_channels = len(channel_struct)
    current_channel = 1
    #print(p25_struct['23ce07']['name'])

    ################################################
    #length
    #dealing with channel struct
    #print(channel_struct)
    #for key in channel_struct:
    #    print(key, '->', channel_struct[key])
    #print("====")
    #print(channel_struct[1]['frequency'])
    ################################################
    #set the initial from the first item in the yaml file
    frequency = channel_struct[current_channel]['frequency']
    mode = channel_struct[current_channel]['mode']
    label = channel_struct[current_channel]['label']
    add_to_image.rectangle(freq_zone, fill="black", outline = "black")
    font = make_font("FreePixel.ttf", 14)
    add_to_image.rectangle(text_zone, fill="black", outline = "black")
    add_to_image.rectangle(mode_zone, fill="black", outline = "white")
    add_to_image.rectangle(label_zone, fill="black", outline = "black")
    add_to_image.text(freq_start, frequency, font=font, fill="white")
    add_to_image.text(mode_start, mode, fill="white")
    add_to_image.text(label_start, label, fill="white")
    ################################################
    print("in mainloop")
    while True:
        data = ser.readline()[:-2] # get rid of newline cr
        if data:
            print(data)

            now = datetime.datetime.now(pytz.timezone('US/Central'))
            print (now.strftime("%Y-%m-%d %H:%M:%S"))


            add_to_image.rectangle(rssi_zone, fill="black", outline = "white")
            add_to_image.text(rssi_start, "---", fill="white")
            add_to_image.rectangle(time_zone, fill="black", outline = "black")
            add_to_image.text(time_start, now.strftime("%H:%M:%S") , fill="white")
            #add_to_image.rectangle(mode_zone, fill="black", outline = "white")
            #add_to_image.text(mode_start, mode , fill="white")

            #print default of first channel
            if (current_state == "idle"):
                frequency = channel_struct[current_channel]['frequency']
                mode = channel_struct[current_channel]['mode']
                label = channel_struct[current_channel]['label']

                #add_to_image.rectangle(freq_zone, fill="black", outline = "white")
                #font = make_font("FreePixel.ttf", 14)
                #add_to_image.text(freq_start, frequency, font=font, fill="white")

                #this is the data box below
                #add_to_image.rectangle(text_zone, fill="black", outline = "black")
                #font = make_font("FreePixel.ttf", 10)
                #add_to_image.text(text_start, "trunk: grnshf\n1: nrcs", font=font, fill="white")



            #if (data == b'k'):
            #    add_to_image.rectangle(freq_zone, fill="black", outline = "white")
            #    font = make_font("FreePixel.ttf", 14)
            #    add_to_image.text(freq_start, frequency, font=font, fill="white")
            #    add_to_image.rectangle(text_zone, fill="black", outline = "black")
            #    trunk1()



            #user pressed the UP button -- next channel
            if (data == b'U'):
                if (current_channel == total_channels):
                    #at the end of the list, start over
                    current_channel = 1
                else:
                    current_channel = current_channel + 1

                frequency = channel_struct[current_channel]['frequency']
                mode = channel_struct[current_channel]['mode']
                label = channel_struct[current_channel]['label']

                add_to_image.rectangle(freq_zone, fill="black", outline = "white")
                font = make_font("FreePixel.ttf", 14)
                add_to_image.rectangle(text_zone, fill="black", outline = "black")
                add_to_image.rectangle(mode_zone, fill="black", outline = "white")
                add_to_image.rectangle(label_zone, fill="black", outline = "white")
                add_to_image.text(freq_start, frequency, font=font, fill="white")
                add_to_image.text(mode_start, mode, fill="white")
                add_to_image.text(label_start, label, fill="white")
                #trunk1()


            #user pressed the DOWN button -- next channel
            if (data == b'D'):
                if (current_channel == 1):
                    #at the start of the list, go to end
                    current_channel = total_channels
                else:
                    current_channel = current_channel - 1

                frequency = channel_struct[current_channel]['frequency']
                mode = channel_struct[current_channel]['mode']
                label = channel_struct[current_channel]['label']

                add_to_image.rectangle(freq_zone, fill="black", outline = "white")
                font = make_font("FreePixel.ttf", 14)
                add_to_image.rectangle(text_zone, fill="black", outline = "black")
                add_to_image.rectangle(mode_zone, fill="black", outline = "white")
                add_to_image.rectangle(label_zone, fill="black", outline = "white")
                add_to_image.text(freq_start, frequency, font=font, fill="white")
                add_to_image.text(mode_start, mode , fill="white")
                add_to_image.text(label_start, label, fill="white")
                #trunk1()


            #user wants that channel
            if (data == b'i'):
                if (current_state == "receive"):
                    #kill the current process
                    current_state = "idle"
                    command = channel_struct[current_channel]['command']
                    print("killing pid", PID.pid)
                    os.killpg(os.getpgid(PID.pid), signal.SIGTERM)
                    add_to_image.rectangle(rssi_zone, fill="black", outline = "white")
                    add_to_image.text(rssi_start, "---", fill="white")
                else:
                    #start the receive process
                    current_state = "receive"
                    command = channel_struct[current_channel]['command']
                    PID = do_receive(command)
                    print("started", command, "at pid", PID.pid)
                    add_to_image.rectangle(rssi_zone, fill="black", outline = "black")
                    add_to_image.text(rssi_start, "RX", fill="white")


            ####last line of if data
            device.display(output)

        #update time once per second
        if ((time.time() > (start_time + 1))):
            now = datetime.datetime.now(pytz.timezone('US/Central'))
            add_to_image.rectangle(time_zone, fill="black", outline = "black")
            add_to_image.text(time_start, now.strftime("%H:%M:%S") , fill="white")
            device.display(output)



################################################################################
#mqtt initialization
################################################################################
def mqtt_init():
    client = mqttClient.Client("Python")
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port=1883)
    client.loop_start()
    while Connected != True:
        print("not connected")
        time.sleep(0.1)
    print(client.subscribe('mqtt/p25'))



################################################################################
#do_receive
#   function to start a command and return the PID    
################################################################################
def do_receive(command):
    time.sleep(1)
    #proc = subprocess.Popen(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
    #print("started", command, "at pid", proc.pid)
    return proc


################################################################################
################################################################################
def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)



################################################################################
################################################################################
def read_configfile(yamlfile):
    with open(yamlfile, "r") as f:
        data_loaded = yaml.load(f)
    return data_loaded


################################################################################
#only update the UNIT on change
################################################################################
def on_message(client, userdata, message):
    global UNIT
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
    if re.match(r".+NAC 0x230", message.payload.decode('ISO-8859-1')):
        #print message.payload.split("=")
        r = message.payload.split(b"=")
        temp = show_last_call(r[5][2:])
        #only change the unit number when the caller changes:w
        if (temp != UNIT):
            UNIT = temp
            print(UNIT)
            now = datetime.datetime.now(pytz.timezone('US/Central'))
            to_print = now.strftime("%H:%M:%S") + " " + UNIT
            add_to_image.rectangle(text_zone, fill="black", outline = "black")
            add_to_image.text(text_start1, to_print , fill="white")

    #if this is EMS
    if re.match(r".+NAC 0x231", message.payload.decode('ISO-8859-1')):
        #print message.payload.split("=")
        r = message.payload.split(b"=")
        UNIT = show_last_call(r[5][2:])


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
#show_last_call
#   decode the RID to a value defined in cops.yaml
#################################################################################
def show_last_call(radio_id):
    p25_struct = read_configfile('/home/timc/bct8-upgrade/misc/cops.yaml')
    radio_id = radio_id.strip()
    radio_id = radio_id.decode('ISO-8859-1')
    #if (p25_struct[radio_id]):
    try:
        id = p25_struct[radio_id]['name']
        #print("testing", p25_struct[radio_id]['name'])
        #print(id)
        return(id)
    except:
        id = "RID:" + radio_id
        #print(id)
        return(id)
    



################################################################################
def main():
    mqtt_init()
    mainloop(device)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass











# temp_ext
#temp_c=33
#temp_zone = [(14,44), (36,64)]
#temp_start = (14,44)
#temp_icon_zone = [(0,48), (15,64)]
#temp_icon_start = (3,48)
##add_to_image.text(temp_icon_start, "\uf2c9", font=FA_solid, fill="white")
#add_to_image.text(temp_icon_start, "test", fill="white")
#
#### every time I have a new reading, I basically draw a black rectangle over what I had and the rewrite the text
#add_to_image.rectangle(temp_zone, fill="black", outline = "black")
#add_to_image.text(temp_start, str(temp_c), fill="white")
#device.display(output)
#
#sleep(5)

#temp_c=34
#add_to_image.rectangle(temp_zone, fill="black", outline = "black")
#add_to_image.text(temp_start, str(temp_c), fill="white")
#device.display(output)


#sleep(10)
