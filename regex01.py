#!/usr/bin/env python
#practice regex
import re

file = open('web_blink.py')
for line in file:
    line = line.rstrip()
    if re.search('#', line) :
        print line
 
