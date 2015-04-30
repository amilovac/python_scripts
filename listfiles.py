#!/usr/bin/python

# get the list of file with certain extension
# amilovac 7. April 2015


import os
from os.path import join
for (dirname, dirs, files) in os.walk(' . ' ):
    for filename in files:
        if filename.endswith(' .txt' ):
            thefile = os.path.join(dirname,filename)
            print os.path.getsize(thefile), thefile
