#!/usr/bin/python3

################################################################################
#scan_client3.py
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

#mqtt stuff
import paho.mqtt.client as mqttClient
Connected = False
broker = "localhost"

hd_audio_channel = -1
PID = 0

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
text_start = (2,42)

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
    channel_struct = read_configfile()
    total_channels = len(channel_struct)
    current_channel = 1

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
    add_to_image.rectangle(freq_zone, fill="black", outline = "white")
    font = make_font("FreePixel.ttf", 14)
    add_to_image.rectangle(text_zone, fill="black", outline = "black")
    add_to_image.rectangle(mode_zone, fill="black", outline = "white")
    add_to_image.rectangle(label_zone, fill="black", outline = "white")
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
            add_to_image.text(rssi_start, "..!!", fill="white")
            add_to_image.rectangle(time_zone, fill="black", outline = "white")
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
                    print("kill ")
                    print(command)
                    print("\n")
                else:
                    #start the receive process
                    current_state = "receive"
                    command = channel_struct[current_channel]['command']
                    do_receive(command)


            ####last line of if data
            device.display(output)

        #update time once per second
        if ((time.time() > (start_time + 1))):
            now = datetime.datetime.now(pytz.timezone('US/Central'))
            add_to_image.rectangle(time_zone, fill="black", outline = "white")
            add_to_image.text(time_start, now.strftime("%H:%M:%S") , fill="white")
            device.display(output)



################################################################################
################################################################################
def do_receive(command):
    global PID
    time.sleep(1)
    print("starting ")
    print(command)
    print("\n")
    if (PID):
        os.kill(PID, signal.SIGTERM)
    PID = subprocess.Popen(command)


################################################################################
################################################################################
def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)



################################################################################
################################################################################
def read_configfile():
    with open("scannerlist.yaml", "r") as f:
        data_loaded = yaml.load(f)
    return data_loaded



################################################################################
def main():
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
