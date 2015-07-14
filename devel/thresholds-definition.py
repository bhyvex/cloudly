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
            'range_min': 0,
            'range_max': 55,
        },
        "WARNING": {
            'range_min': 56,
            'range_max': 90,
            'duration_in_seconds': 'tbd',
        },
        "CRITICAL": {
            'range_min': 90,
            'duration_in_seconds': 'tbd',
        },
    }

    loadavg=subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg = re.findall(r"(\d+\.\d{2})", loadavg)

    # XXX nagios like message


    return loadavg
    

    

print _get_sys_loadavg()





