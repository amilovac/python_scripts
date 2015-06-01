#!/usr/bin/env python
import os
# find and remove file in directory

for (root,files,subdirs) in os.walk('/home/pi/vezbanja'):
    for file in files:
        print (file) 
        if '.rpmsave' in file:
            os.remove(file)
