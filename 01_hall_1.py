#!/usr/bin/env python
import RPi.GPIO as GPIO

HALL = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(HALL,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def magnet_detected(channel):
        print "Magnetic material detected"  

GPIO.add_event_detect(HALL, GPIO.FALLING, callback=magnet_detected)

try:
    while True:
        pass

except KeyboardInterrupt:
    print "Ctrl-C - quit"

finally:
    GPIO.cleanup() 

