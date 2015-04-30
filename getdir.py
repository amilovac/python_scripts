#!/opt/swe/tools/ext/gnu/python-2.7.8/i686-linux2.6/bin/python -u

import subprocess
import os

# dictionary to keep the result
parsed = {}
get_dir = list()
# get my pwd
# kako koristiti dicts - kao asocijativne nizove u php? data = {}
# data['host'] = my_hostname   
#  data['type'] = 'special'
# json.dumps(data) - baci ga u json


try:
    print 'My current dir is:'+ os.getcwd()
    print "Listing the content....\n"
except:
    print "Couldn't get the current dir. Exiting..."
    exit()
get_dir= subprocess.check_output(['ls','-lah'])

print get_dir


