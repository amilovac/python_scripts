#!/usr/bin/env python

import subprocess

cmd_str = 'echo "amilovac"'

cmd = cmd_str.split()
retcode = subprocess.call(cmd)
retcode = subprocess.check_call(cmd)
output = subprocess.check_output(cmd)
