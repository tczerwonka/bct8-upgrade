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
frequency = 146520000

current_state = 'idle'
start_time = time.time()



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

text_zone = [(0,41), (127,63)]
text_start = (2,44)

#next line -- frequency
#next lines -- data -- 3 line buffer?
################################################################################

mode = "P25"
start_time = time.time()

################################################################################
################################################################################

def mainloop(device):
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
            add_to_image.rectangle(mode_zone, fill="black", outline = "white")
            add_to_image.text(mode_start, mode , fill="white")

            add_to_image.rectangle(freq_zone, fill="black", outline = "white")
            font = make_font("FreePixel.ttf", 14)
            add_to_image.text(freq_start, "154.7750", font=font, fill="white")

            add_to_image.rectangle(text_zone, fill="black", outline = "white")


            device.display(output)
        if ((time.time() > (start_time + 1))):
            now = datetime.datetime.now(pytz.timezone('US/Central'))
            add_to_image.rectangle(time_zone, fill="black", outline = "white")
            add_to_image.text(time_start, now.strftime("%H:%M:%S") , fill="white")
            device.display(output)




################################################################################
################################################################################
def make_font(name, size):
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', name))
    return ImageFont.truetype(font_path, size)



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
