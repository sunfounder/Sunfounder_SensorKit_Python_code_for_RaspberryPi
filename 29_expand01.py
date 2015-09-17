#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import os
import sys

# Define RGB LED pin
LedRed    = 11
LedGreen  = 12
LedBlue   = 13

# Define Buzzer pin
Buzzer = 15

def beep(x):
	GPIO.output(Buzzer, 0)
	time.sleep(x)
	GPIO.output(Buzzer, 1)
	time.sleep(x)

def tempRead():
	global ds18b20
	address = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(address)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def ds18b20Init():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i[:2] == '28':
			ds18b20 = i

def setup():
	GPIO.setmode(GPIO.BOARD)
	# Buzzer setup:
	GPIO.setup(Buzzer, GPIO.OUT)
	GPIO.output(Buzzer, 1)
	# RGB setup:
	GPIO.setup(LedRed, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(LedGreen, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(LedBlue, GPIO.OUT, initial=GPIO.LOW)
	# DS18B20 setup:
	ds18b20Init()

def loop():
	if len(sys.argv) != 3:
		print 'Usage:'
		print '    sudo python 29_expand01.py [temperature lower limit] [upper limit]'
		print 'For example: sudo python 29_expand01.py 29 31\n'
		destroy()
		quit()
	low = float(sys.argv[1])
	high = float(sys.argv[2])
	if low >= high:
		print 'Parameters error, lower limit should be less than upper limit'
		destroy()
		quit()
	print 'System is running...'
	print 'The lower limit of temperature:', low
	print 'The upper limit of temperature:', high
	
	while True:
		# Read temperature from ds18B20
		temp = tempRead()
		print 'Current temperature:', temp

		# Under/Over limit alarm:
		if temp < low:
			GPIO.output(LedBlue, 1);
			GPIO.output(LedRed, 0);
			GPIO.output(LedGreen, 0);
			for i in range(0, 4):
				beep(0.25)

		if temp >= low and temp < high:
			GPIO.output(LedBlue, 0);
			GPIO.output(LedRed, 0);
			GPIO.output(LedGreen, 1);
			time.sleep(1)

		if temp >= high:
			GPIO.output(LedBlue, 0);
			GPIO.output(LedRed, 1);
			GPIO.output(LedGreen, 0);
			for i in range(0, 8):
				beep(0.125)

def destroy():
	GPIO.output(LedRed, 0)
	GPIO.output(LedGreen, 0)
	GPIO.output(LedBlue, 0)
	GPIO.output(Buzzer, 1)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
