#!/bin/sh
/usr/local/bin/rtl_udp -f 93.7M -s 260k -r 48000 -g 50 -o 1 - | aplay -r 48000 -f S16_LE -c 1 -q  -V mono -D sysdefault:CARD=ALSA
