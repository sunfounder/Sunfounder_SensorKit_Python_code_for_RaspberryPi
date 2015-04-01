#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

FlamePin = 11

def init():
	GPIO.setmode(GPIO.BOARD)	
	GPIO.setup(FlamePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def myISR(ev=None):
	print "Flame is detected !"

def loop():
	GPIO.add_event_detect(FlamePin, GPIO.FALLING, callback=myISR)
	while True:
		pass

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		print 'The end !'
