#!/usr/bin/python

subprocess.Popen(('find', '/tmp/mount', '-type', 'f',
                  '-name', '*.rpmsave', '-exec', 'rm', '-f', '{}', ';'))
