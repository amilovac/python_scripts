#!/usr/bin/env python
import os
# find and remove file in directory
#FILE_PATERN = "web_blink.py"
for (root,files,subdirs) in os.walk('/home/pi/scripts'):
    for file in files:
        if 'hooks' in file: 
            print "I have found the: %s in: %s!" % (file, root) 
