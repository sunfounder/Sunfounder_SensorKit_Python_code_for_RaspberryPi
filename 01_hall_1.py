#!/usr/bin/env python
import RPi.GPIO as GPIO

#Hall sensor is connected to pin 11 (BOARD-Layout!)
HALL = 11 

#LED is connected to pin 12 (BOARD-Layout!)
LED  = 12

#Set pin-layout to BOARD
GPIO.setmode(GPIO.BOARD)

#Avoid error messages if GPIO was not shut down correctly before
GPIO.setwarnings(False) 

#Set HALL-pin to input, use internal pull-up-resistor
GPIO.setup(HALL,GPIO.IN, pull_up_down=GPIO.PUD_UP) 

#Set LED-pin to output. A resistor should be used here!
GPIO.setup(LED, GPIO.OUT)

#Turn LED off
GPIO.output(LED, GPIO.LOW)

#This function will be called if a change is detected
def change_detected(channel):
    if GPIO.input(HALL) == GPIO.LOW:
        print 'Magnetic material detected: LED on'
        GPIO.output(LED, GPIO.HIGH) #LED on
    else:
        print 'No magnetic material: LED off'
	GPIO.output(LED, GPIO.LOW) # LED off

# Register event-listener on falling and raising
# edge on HALL-sensor input. Call "change_detected" as
# callback
GPIO.add_event_detect(HALL, GPIO.BOTH, change_detected, bouncetime=25)

# The main-loop does nothing. All is done by the event-listener
try:
    while True:
        pass

# Quit on Ctrl-c
except KeyboardInterrupt:
    print "Ctrl-C - quit"

# Cleanup GPIO
finally:
    GPIO.cleanup() 

