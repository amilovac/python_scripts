#!/usr/bin/env python
import re

x = '2 omiljena broja su 34 i 56'
y = re.findall('[0-9]+', x)
print y 

