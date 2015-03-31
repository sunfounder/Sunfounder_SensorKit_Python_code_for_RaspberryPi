#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

ADC_CS  = 11
ADC_CLK = 12
ADC_DIO = 13

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location
	GPIO.setup(ADC_CS, GPIO.OUT)
	GPIO.setup(ADC_CLK, GPIO.OUT)

def destroy():
	GPIO.cleanup()

def getResult():     # get ADC result
	GPIO.setup(ADC_DIO, GPIO.OUT)
	GPIO.output(ADC_CS, 0)
	
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)

	GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
	GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)

	GPIO.output(ADC_DIO, 0);  time.sleep(0.000002)

	GPIO.output(ADC_CLK, 1)
	GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
	GPIO.output(ADC_CLK, 0)
	GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
	
	dat1 = 0
	for i in range(0, 8):
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0);  time.sleep(0.000002)
		GPIO.setup(ADC_DIO, GPIO.IN)
		dat1 = dat1 << 1 | GPIO.input(ADC_DIO)  # or ?
	
	dat2 = 0
	for i in range(0, 8):
		dat2 = dat2 | GPIO.input(ADC_DIO) << i
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0);  time.sleep(0.000002)
	
	GPIO.output(ADC_CS, 1)
	GPIO.setup(ADC_DIO, GPIO.OUT)

	if dat1 == dat2:
		return dat1
	else:
		return 0

def loop():
	while True:
		res = getResult()
		print 'res = %d' % res
		time.sleep(0.4)

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

