#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time
import os

# Define RGB LED pin
LedRed    = 15
LedGreen  = 16
LedBlue   = 18

# Define Joystick button pin
btn = 22

# Define Buzzer pin
Buzzer = 3

def beep(x):
	GPIO.output(Buzzer, 0)
	time.sleep(x)
	GPIO.output(Buzzer, 1)
	time.sleep(x)

def tempRead():
	global ds18b20
	address = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(address)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def joystickbtn(ev=None):
	print 'Interrupt occur!'
	destroy()

def joystickState():
	if ADC0832.getResult1() == 0:
		return 1		#up
	if ADC0832.getResult1() == 255:
		return 2		#down
	if ADC0832.getResult() == 0:
		return 3		#left
	if ADC0832.getResult() == 255:
		return 4		#right

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def ds18b20Init():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1-bus-master1':
			ds18b20 = i

def setup():
	GPIO.setmode(GPIO.BOARD)
	# Buzzer setup:
	GPIO.setup(Buzzer, GPIO.OUT)
	GPIO.output(Buzzer, 1)
	# RGB setup:
	GPIO.setup(LedRed, GPIO.OUT)
	GPIO.setup(LedGreen, GPIO.OUT)
	GPIO.setup(LedBlue, GPIO.OUT)
	GPIO.output(LedRed, 1)
	GPIO.output(LedGreen, 1)
	GPIO.output(LedBlue, 1)
	# DS18B20 setup:
	ds18b20Init()
	# Joystick setup:
	GPIO.setup(btn, GPIO.IN)
	GPIO.add_event_detect(btn, GPIO.FALLING, callback=joystickbtn, bouncetime=200)
	# ADC0832 setup:
	ADC0832.setup()

def loop():
	low = 28
	high = 32
	print 'System is running...'


	while True:
		# Change low/high limit with Joystick
		joystick = joystickState()
		print joystick

		if joystick == 1 and low < high - 1:
			low += 1
		if joystick == 2 and low > 0:
			low -= 1
		if joystick == 4 and high > low + 1:
			high -= 1
		if joystick == 3 and high < 125:
			high += 1

		print 'The lower limit of temperature:', low
		print 'The upper limit of temperature:', high

		# Read temperature from ds18B20
		temp = tempRead()
		print 'Current temperature:', temp

		# Under/Over limit alarm:
		if temp < low:
			GPIO.output(LedBlue, 0);
			GPIO.output(LedRed, 1);
			GPIO.output(LedGreen, 1);
			for i in range(0, 4):
				beep(0.25)

		if temp >= low and temp < high:
			GPIO.output(LedBlue, 1);
			GPIO.output(LedRed, 1);
			GPIO.output(LedGreen, 0);
			time.sleep(1)

		if temp >= high:
			GPIO.output(LedBlue, 1);
			GPIO.output(LedRed, 0);
			GPIO.output(LedGreen, 1);
			for i in range(0, 8):
				beep(0.125)

def destroy():
	GPIO.output(LedRed, 1)
	GPIO.output(LedGreen, 1)
	GPIO.output(LedBlue, 1)
	GPIO.output(Buzzer, 1)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
