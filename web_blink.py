#!/usr/bin/env python
# Test to see if we have working internet connection 
import socket
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
REMOTE_SERVER = "www.google.com"

#turn off LED
enable_led(False)
# check connection function
# returns True if site is reachable and name can be resolved
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
if (is_connected()):

    print 'Internet connected? Trying to connect to google... %s' %(is_connected())
    enable_led(True)
    print "LED is ON"

    sleep(5)
GPIO.cleanup()
