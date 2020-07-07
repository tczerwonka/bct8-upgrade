#!/bin/sh
#wbfm -- 260k?
#/usr/local/bin/rtl_udp -f 93.7M -s 260k -r 48000 -g 50 -o 1 - | aplay -r 48000 -f S16_LE -c 1 -q  -V mono -D sysdefault:CARD=ALSA

#/usr/local/bin/rtl_udp -f 146.52M -s 8000 -g 50 -o 1 - | aplay -r 8000 -f S16_LE -c 1 -q  -V mono -D sysdefault:CARD=ALSA

/usr/local/bin/rtl_udp -f 146.52M  -o 4 -C -l 220 -s 24k - | aplay -r 24000 -f S16_LE -c 1 -q  -V mono -D sysdefault:CARD=ALSA

    #[-s sample_rate (default: 24k)]
    #[-r output_rate (default: same as -s)]
    #[-g tuner_gain (default: automatic)]
    #[-l squelch_level (default: 0/off)]
    #[-N enables NBFM mode (default: on)]
    #[-W enables WBFM mode (default: off)]
    # (-N -s 170k -o 4 -A fast -r 32k -l 0 -D)
    #[-D enables de-emphasis (default: off)]
    #[-C enables DC blocking of output (default: off)]
    #[-A std/fast/lut choose atan math (default: std)]

