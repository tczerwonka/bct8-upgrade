#!/usr/bin/python3

from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep

serial = i2c(port=1, address=0x3C)

device=ssd1306(serial)

#with canvas(device) as draw:
#    draw.rectangle(device.bounding_box, outline="white", fill="black")
#    draw.text((30, 40), "Hello World", fill="white")

#works
#with canvas(device) as draw:
#    draw.rectangle((0, 10, 127, 63), outline="white")
#    draw.text((10, 40), "Hello World", fill="white")

canvas(device).rectangle((0,0,127,63), outline="white")

sleep(10)
