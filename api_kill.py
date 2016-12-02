import re, os
import subprocess

ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE, close_fds=True).communicate()[0]

for line in ps.split('\n'):
    if "api.py" in line:
        print line
