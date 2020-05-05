# bct8-upgrade
Code to replace the guts of a Uniden BCT8 with a pi and rtl-sdr.

I purchased a Uniden BCT8 scanner that wasn't working, thinking I 
could repair it.  I believe the problem is actually the IF filters
which are both bad and unobtanium.

This project removes the receiver hardware and replaces it with
an arduino to control the face panel and a pi with an rtlsdr for
the radio hardware.

Status:

Special elements seem to work, need to figure out how to turn off.

Alpha-numeric character string works.  Need to finish letters.

Number handling is OK, could be more robust.

## display_testing  

Arduino code -- screwing around to test stuff

## front_panel_client

More useful.

Front panel keys send a character.

Send unprefixed alpha characters to display on screen in left
three digits.

Prefix with # for a number.

Prefix with ! for special character.

### Special Characters

MRN, MLO, RMT, ATT, RR, AIR, CB, NWS, BN2, BN1, BNX, BN3, BN4, BN5, PVT, POL, WX, FIR, M, E, L, LST, TRK, HWY, SRH, HLD, P, DN, PRI, DEC, LO, DLY, DTA, FLS

Note that writing to a character shared with a special character will
cause some corruption at the moment, e.g. sending

HAM -- print 'HAM'
!P -- will light the "P" -- but corrupts the left letter in 'HAM'.

