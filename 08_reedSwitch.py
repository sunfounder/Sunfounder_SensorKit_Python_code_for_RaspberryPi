#!/usr/bin/env python
import RPi.GPIO as GPIO

ReedPin = 11
LedPin  = 12

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(ReedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led

def switchLed(channel):
	if GPIO.input(11):
		print "Magnet detected - LED on!"
		GPIO.output(LedPin,GPIO.HIGH)
	else:
		print "No magnet detected - LED off!"
		GPIO.output(LedPin,GPIO.LOW)

def loop():
	GPIO.add_event_detect(ReedPin,GPIO.BOTH, callback=switchLed, bouncetime=20)
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


