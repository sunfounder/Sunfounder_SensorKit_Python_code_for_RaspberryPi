#!/usr/bin/env python
import RPi.GPIO as GPIO

SIG = 11
LED = 12

Led_status = 1

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LED, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(SIG, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LED, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def loop():
	while True:
		if(0 == GPIO.input(SIG)):
			GPIO.output(LED, GPIO.HIGH)
		else:
			GPIO.output(LED, GPIO.LOW)

def destroy():
	GPIO.output(LED, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

