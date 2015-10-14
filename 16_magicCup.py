#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

MERCURY_SIG1 = 11
LED1 = 12

LED2 = 15


def setup():
	global p_LED1, p_LED2
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(MERCURY_SIG1, GPIO.IN)
	GPIO.setup(LED1, GPIO.OUT)
	GPIO.setup(LED2, GPIO.OUT)

	p_LED1 = GPIO.PWM(LED1, 200)
	p_LED2 = GPIO.PWM(LED2, 200)
	
	p_LED1.start(0)
	p_LED2.start(0)
	
def loop():
	led1_value = 0
	led2_value = 0
	while True:
		mercury_value = GPIO.input(MERCURY_SIG1)
		if mercury_value == 0:
			led1_value -= 1
			led2_value += 1
			if led1_value < 0:
				led1_value = 0
			if led2_value > 100:
				led2_value = 100
		
		if mercury_value == 1:
			led1_value += 1
			led2_value -= 1
			if led1_value > 100:
				led1_value = 100
			if led2_value < 0:
				led2_value = 0
				
		p_LED1.ChangeDutyCycle(led1_value)
		p_LED2.ChangeDutyCycle(led2_value)
		time.sleep(0.05)
		
def destroy():
	p_LED1.stop()
	p_LED2.stop()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
	
		


