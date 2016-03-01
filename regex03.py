#!/usr/bin/env python
import re
file = open('test.txt')
for line in file:
    y = re.findall('\S+@\S+', line)
    print y
