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

 
def _get_disks_usage():

    disks_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 90,
            'max_value': 95,
            'min_duration_in_seconds': 1,
        },
        "CRITICAL": { # is everything above the warning range
            'min_duration_in_seconds': 1,
        },
    }
    service_status = {
        'status': '',
        'service': 'system_disks',
    }

    proc = subprocess.Popen(['df', '-B 1'], stdout=subprocess.PIPE, close_fds=True)
    df = proc.communicate()[0] 

    try:
        volumes = df.split('\n')
        volumes.pop(0)
        volumes.pop()
    except: return {"error":True,"error_description":"_get_disks_usage"}

    regexp = re.compile(r'([0-9]+)')
    previousVolume = None
    volumeCount = 0
    disks_usage = []
    
    for volume in volumes:
        
        volume = volume.split(None, 10)
        
        if len(volume) == 1:
            previousVolume = volume[0]
            continue
        
        if previousVolume != None:
            volume.insert(0, previousVolume) 
            previousVolume = None
        
        volumeCount = volumeCount + 1
        
        if regexp.match(volume[1]) == None:
            pass
        
        else:
            try:
                volume[2] = int(volume[2]) # Used
                volume[3] = int(volume[3]) # Available
            except IndexError:
                pass
            except KeyError:
                pass
            
            disks_usage.append(volume)
    

    for disk in disks_usage:
    
        status = 'UNKNOWN'

        print disk[4]


    
    
    return disks_usage


import pprint
#pprint.pprint( _get_disks_usage() )
_get_disks_usage()


