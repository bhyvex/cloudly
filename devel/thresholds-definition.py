# -*- coding: utf-8
#!/usr/bin/env python

import os
import sys
import re
import time
import socket
import getpass
import datetime
import platform
import base64, pickle

import urllib
import httplib
import subprocess


try:
    import json
except: pass



def _get_sys_loadavg():

    threshold_definition = {
        "OK": {},
        "WARNING": {
            'min_range': 1,
            'max_range': 1.5,
            'min_duration_in_seconds': 60,
        },
        "CRITICAL": { # is everything above the warning range
            'min_duration_in_seconds': 20,
        },
    }

    loadavg=subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg = re.findall(r"(\d+\.\d{2})", loadavg)

    # XXX analyze and work in nagios like output message


    return loadavg
    

    

print _get_sys_loadavg()





