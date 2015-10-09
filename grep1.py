#!/usr/bin/env python

import subprocess

cmd = "grep CHECKOUT_REVISION /home/eday/test.txt | cut -d'\"' -f2 -s"
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()[0]

print (temp)
