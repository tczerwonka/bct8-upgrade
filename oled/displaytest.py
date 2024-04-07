#!/usr/bin/python3

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont, Image, ImageDraw    
from time import sleep

device=ssd1306(i2c(port=1, address=0x3C))
device.clear()

#with canvas(device) as draw:
#    draw.rectangle(device.bounding_box, outline="white", fill="black")
#    draw.text((30, 40), "Hello World", fill="white")

#with canvas(device) as draw:
#    draw.rectangle((0, 10, 127, 63), outline="white")
#    draw.text((10, 40), "Hello World", fill="white")

#works
#with canvas(device) as draw:
#    draw.rectangle((0,10,127,63), outline="white")
#    draw.text((10, 40), "Hello World", fill="white")


#uses PIL with image zones, hm.
### Initialize drawing zone (aka entire screen)
output = Image.new("1", (128,64))
add_to_image = ImageDraw.Draw(output)

### I have the exterior temp and altitude I want to display. Each has an assigned zone for the icon (FontAwesome) and the data
# temp_ext
temp_c=33
temp_zone = [(14,44), (36,64)]
temp_start = (14,44)
temp_icon_zone = [(0,48), (15,64)]
temp_icon_start = (3,48)
#add_to_image.text(temp_icon_start, "\uf2c9", font=FA_solid, fill="white")
add_to_image.text(temp_icon_start, "test", fill="white")

### every time I have a new reading, I basically draw a black rectangle over what I had and the rewrite the text
add_to_image.rectangle(temp_zone, fill="black", outline = "black")
add_to_image.text(temp_start, str(temp_c), fill="white")
device.display(output)

sleep(5)

temp_c=34
add_to_image.rectangle(temp_zone, fill="black", outline = "black")
add_to_image.text(temp_start, str(temp_c), fill="white")
device.display(output)


sleep(10)
