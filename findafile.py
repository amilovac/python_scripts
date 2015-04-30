#!/usr/bin/python

# find and remove file in directory

for (root,files,subdirs) in os.walk('/tmp/mount'):
    for file in files:
        if '.rpmsave' in file:
            os.remove(file)
