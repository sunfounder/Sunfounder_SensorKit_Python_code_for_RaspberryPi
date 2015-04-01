#!/usr/bin/env python

#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#----------------------------------------------------------------
tfile = open("/sys/bus/w1/devices/28-00145232cfff/w1_slave")
text = tfile.read()
tfile.close()
secondline = text.split("\n")[1]
temperaturedata = secondline.split(" ")[9]
temperature = float(temperaturedata[2:])
temperature = temperature / 1000
print "Current temperature : %0.3f C" % temperature
