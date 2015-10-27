#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

'''
 Example how to use the hall-sensor with digital and analog output
 While the loop is printing the analog values, an interrupt-method
 is waiting for changes on the digital pin. In case of any change
 the message "change detected" is displayed.

 Example output:
 res0 = 138, res1 = 0
 res0 = 133, res1 = 0
 Change detected
 res0 = 116, res1 = 0
 Change detected
 res0 = 132, res1 = 0
 res0 = 138, res1 = 0
'''

# Digital out of sensor connected to
# pin 16 (BOAR-Layout!)
HALL = 16 #

#The ADC is connected like described in the manual


GPIO.setmode(GPIO.BOARD) # using BOARD layout 

GPIO.setwarnings(False) 

# Setup pins
GPIO.setup(HALL,GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Callback if digital-out triggers
def change_detected(channel):
    print 'Change detected'

def init():
	ADC0832.setup()

# register event listener
GPIO.add_event_detect(HALL, GPIO.BOTH, change_detected, bouncetime=25)

def loop():
	while True:
                res0 = ADC0832.getResult(0)
		res1 = ADC0832.getResult(1)
		print 'res0 = %d, res1 = %d' % (res0,res1)
		time.sleep(0.2)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()



