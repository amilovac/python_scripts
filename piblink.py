#!/usr/bin/env python

# blinks one led connected to pi GPIO pin
import RPi.GPIO as GPIO
from time import sleep
     
#define the pin and its function
LED_PIN =18 
print "Setting up GPIO"
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

#blink function     
def enable_led(should_enable):
  	if should_enable:
   		GPIO.output(LED_PIN, True)
   	else:
   		GPIO.output(LED_PIN, False)

#start blinking     
enable_led(False)
print "LED is OFF"
sleep(2)
enable_led(True)
print "LED is ON"
sleep(2)
enable_led(False)
print "LED is OFF"
sleep(2)
enable_led(True)
print "LED is ON"
sleep(2)
GPIO.cleanup()
