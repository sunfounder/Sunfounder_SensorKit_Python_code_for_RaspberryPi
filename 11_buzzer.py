#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

BuzzerPin = 11    # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(BuzzerPin, GPIO.OUT)
	GPIO.output(BuzzerPin, GPIO.HIGH)

def loop():
	while True:
		GPIO.output(BuzzerPin, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(BuzzerPin, GPIO.HIGH)
		time.sleep(0.5)

def destroy():
	GPIO.output(BuzzerPin, GPIO.HIGH)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

