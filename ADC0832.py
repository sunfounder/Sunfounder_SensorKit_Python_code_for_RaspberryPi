#!/usr/bin/env python
#-----------------------------------------------------
#
#		This is a program for all ADC Module. It 
#	convert analog singnal to digital signal.
#
#		This program is most analog signal modules' 
#	dependency. Use it like this:
#		`import ADC0832`
#		`sig = ADC0832.getResult(chn)`
#
#	*'chn' should be 0 or 1 represent for ch0 or ch1
#	on ADC0832
#		
#		  ACD1302				  Pi
#			CS ---------------- Pin 11
#			CLK --------------- Pin 12
#			DI ---------------- Pin 13

#			VCC ----------------- 3.3V
#			GND ------------------ GND
#
#-----------------------------------------------------
import RPi.GPIO as GPIO
import time

ADC_CS  = 11
ADC_CLK = 12
ADC_DIO = 13

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)    		# Number GPIOs by its physical location
	GPIO.setup(ADC_CS, GPIO.OUT)		# Set pins' mode is output
	GPIO.setup(ADC_CLK, GPIO.OUT)		# Set pins' mode is output

def destroy():
	GPIO.cleanup()

def getResult(chn):     				# Get ADC result, input channal
	if chn ==0 or chn ==1:
		GPIO.setup(ADC_DIO, GPIO.OUT)
		GPIO.output(ADC_CS, 0)
		
		GPIO.output(ADC_CLK, 0)
		GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0)
	
		GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0)
	
		GPIO.output(ADC_DIO, chn);  time.sleep(0.000002)
	
		GPIO.output(ADC_CLK, 1)
		GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
		GPIO.output(ADC_CLK, 0)
		GPIO.output(ADC_DIO, 1);  time.sleep(0.000002)
	
		dat1 = 0
		for i in range(0, 8):
			GPIO.output(ADC_CLK, 1);  time.sleep(0.000002)
			GPIO.output(ADC_CLK, 0);  time.sleep(0.000002)
			GPIO.setup(ADC_DIO, GPIO.IN)
			dat1 = dat1 << 1 | GPIO.input(ADC_DIO)  
		
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
		res = getResult(0)
		print 'res = %d' % res
		time.sleep(0.4)

def destory():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()

