#!/usr/bin/env python

# Test to see if we have working internet connection 
import socket
from time import sleep

REMOTE_SERVER = "www.google.com"

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

print 'Internet connected? Trying to connect to google... %s' %(is_connected())
sleep(5)
