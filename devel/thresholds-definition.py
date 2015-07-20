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
            'min_value': 90,
            'max_value': 100,
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
    
    if(float(cpu_usage['cpu_used']) < cpu_thresholds['WARNING']['min_value']):
        status = 'OK'
    elif(float(cpu_usage['cpu_used']) > cpu_thresholds['WARNING']['min_value'] and float(cpu_usage['cpu_used']) <= cpu_thresholds['WARNING']['max_value']):
        status = 'WARNING'
    else:
        status = 'CRITICAL'

    message = 'The CPU(s) are '
    if(status == 'OK'): message = message + 'within limits: '
    if(status == 'WARNING' or status == 'CRITICAL'): 
        message = status + ' - ' + message + 'quite heavily utilized: '

    message += str(cpu_usage)

    service_status['status'] = status
    service_status['message'] = message

    service_report = {}
    service_report['service_thresholds'] = cpu_thresholds
    service_report['service_status'] = service_status
    
    return cpu_usage, service_report
    


def _get_memory_usage():
    
    memory_free = ""
    memory_total = ""

    memory_info = subprocess.Popen(["cat","/proc/meminfo"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    for element in memory_info.split('\n'):
        if("MemTotal" in element): memory_total = element
        if("MemFree" in element): memory_free = element

    try:
        memory_total = long(memory_total.split(' ')[-2:-1][0]) * 1024
        memory_free = long(memory_free.split(' ')[-2:-1][0]) * 1024
        memory_used = long(memory_total-memory_free)
    except:
        memory_total = -1
        memory_free = -1
        memory_used = -1

    memory_usage = {
        'memory_total': memory_total,
        'memory_free': memory_free,
        'memory_used': memory_used,        
        'memory_used_percentage': round(float(memory_used)/float(memory_total)*100,2),
        'swap_total': 0,
        'swap_used': 0,
        'swap_free': 0,
        'swap_used_percentage': 0,
    }

    mem_info = subprocess.Popen(['free',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    
    for line in mem_info.split('\n'):

        if('swap' in line.lower()):
            mem_info = re.findall("(\d+)", line)
            memory_usage['swap_total'] = long(mem_info[0]) * 1024
            memory_usage['swap_used'] = long(mem_info[1]) * 1024
            memory_usage['swap_free'] = long(mem_info[2]) * 1024
            try:
                memory_usage['swap_used_percentage'] = round(float(mem_info[1])/float(mem_info[0])*100,2)
            except:
                memory_usage['swap_used_percentage'] = 0
    
    return memory_usage




import pprint
pprint.pprint( _get_memory_usage() )


