#!/usr/bin/env python
import RPi.GPIO as GPIO

LightBreakPin = 11
LedPin = 12

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(LightBreakPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW) # Set LedPin low to off led

def swLed(channel):
	status = GPIO.input(LightBreakPin)
	print "LED: on" if status else "LED: off"
	GPIO.output(LedPin,status)

def loop():
	GPIO.add_event_detect(LightBreakPin, GPIO.BOTH, callback=swLed) # wait for falling
	while True:
		pass
def destroy():
	GPIO.output(LedPin, GPIO.LOW)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

