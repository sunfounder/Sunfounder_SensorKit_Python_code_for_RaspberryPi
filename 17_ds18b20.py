#!/usr/bin/env python
import os
import time

#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#----------------------------------------------------------------

# Reads temperature from sensor and prints to stdout
# id is the id of the sensor
def readSensor(id):
	tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	print "Sensor: " + id  + " - Current temperature : %0.3f C" % temperature


# Reads temperature from all sensors found in /sys/bus/w1/devices/
# starting with "28-...
def readSensors():
	count = 0
	sensor = ""
	for file in os.listdir("/sys/bus/w1/devices/"):
		if (file.startswith("28-")):
			readSensor(file)
			count+=1
	if (count == 0):
		print "No sensor found! Check connection"

# read temperature every second for all connected sensors
def loop():
	while True:
		readSensors()
		time.sleep(1)

# Nothing to cleanup
def destroy():
	pass

# Main starts here
if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

