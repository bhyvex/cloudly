import re, os
import subprocess


while True:

    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    for line in ps.split('\n'):
        if "api.py" in line:

            regexp = re.findall(r'(\b[^\s]+\b)', line)
            pid = regexp[1]
            os.system('kill -9 ' + pid)
            print 'api killed...'

    time.sleep(15)
