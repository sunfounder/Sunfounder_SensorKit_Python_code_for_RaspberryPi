#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

MIC_DO_PIN = 15

def init():
	GPIO.setmode(GPIO.BOARD)	
	GPIO.setup(MIC_DO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	ADC0832.setup()

def micISR(ev=None):
	print "voice in..."
	analogVal = ADC0832.getResult()
	print 'res = %d' % res

def loop():
	GPIO.add_event_detect(MIC_DO_PIN, GPIO.FALLING, callback=micISR)
	while True:
		pass

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print 'The end !'
