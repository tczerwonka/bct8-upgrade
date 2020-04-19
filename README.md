# bct8-upgrade
Code to replace the guts of a Uniden BCT8 with a pi and rtl-sdr.

I purchased a Uniden BCT8 scanner that wasn't working, thinking I 
could repair it.  I believe the problem is actually the IF filters
which are both bad and unobtanium.

This project removes the receiver hardware and replaces it with
an arduino ot control the face panel and a pi with an rtlsdr for
the radio hardware.
