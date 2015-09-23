#!/usr/bin/env python
import os
# find and remove file in directory

for (root,files,subdirs) in os.walk('/home/pi/vezbanja'):
    for file in files:
        if 'hooks' in file: 
            print file, root 
