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

    threshold_values = {
        "OK": {
            'range_max': 1,
        },
        "WARNING": {
            'range_max': 1.5,
            'duration_in_seconds': 60,
        },
        "CRITICAL": {
            'duration_in_seconds': 120,
        },
    }

    loadavg=subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg = re.findall(r"(\d+\.\d{2})", loadavg)

    # XXX analyze and work in nagios like output message


    return loadavg
    

    

print _get_sys_loadavg()





