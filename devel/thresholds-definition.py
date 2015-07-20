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

    loadavg_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 1.5,
            'max_value': 3.5,
            'min_duration_in_seconds': 60,
        },
        "CRITICAL": { # is everything above the warning range
            'min_duration_in_seconds': 20,
        },
    }
    service_status = {
        'status': '',
        'service': 'system_loadavg',
    }

    loadavg=subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg = re.findall(r"(\d+\.\d{2})", loadavg)

    status = 'UNKNOWN'
    
    if(float(loadavg[2]) < loadavg_thresholds['WARNING']['min_value']):
        status = 'OK'
    elif(float(loadavg[2]) > loadavg_thresholds['WARNING']['min_value'] and float(loadavg[2]) <= loadavg_thresholds['WARNING']['max_value']):
        status = 'WARNING'
    else:
        status = 'CRITICAL'

    message = 'The System Load is '
    if(status == 'OK'): message = message + 'within limits: '
    if(status == 'WARNING' or status == 'CRITICAL'): message = 'Warning - ' + message

    for i in loadavg: message += str(i) + ' '
    message = message[:-1] 
    message += '.'

    service_status['status'] = status
    service_status['message'] = message

    service_report = {}
    service_report['service_thresholds'] = loadavg_thresholds
    service_report['service_status'] = service_status

    return loadavg, service_report

    

def _get_sys_cpu():
    
    cpu_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 95,
            'max_value': 99,
            'min_duration_in_seconds': 60,
        },
        "CRITICAL": { # is everything above the warning range
            'min_duration_in_seconds': 120,
        },
    }
    service_status = {
        'status': '',
        'service': 'system_cpu',
    }

    cpu_info = subprocess.Popen(["ps","axo","pcpu"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    c=0
    cpu_total = float(0)
    
    for line in cpu_info.split('\n'):

        line = line.replace(' ','')
        
        try:
            cpu_process_usage = float(line)
            cpu_total += cpu_process_usage
        except:
            pass
    
    cpu_usage = {
        'cpu_used':round(cpu_total,2),
        'cpu_free':round(float(100-cpu_total),2)
    }
    
    status = 'UNKNOWN'

    # XXX
    
    return cpu_usage
    

print _get_sys_cpu()

