import os
import sys


def _get_sys_loadavg():

    loadavg=subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg = re.findall(r"(\d+\.\d{2})", loadavg)

    return loadavg
    


def _get_sys_uptime():
    
    uptime = subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    uptime = re.findall("[ 0-9:]up[ ](.*)[,][ 0-9]+user", uptime)[0]

    return uptime
    
    

def _get_sys_cpu():
    
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
    
    return cpu_usage
    

def threshold_values():

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
    
    

    return threshold_values



print threshold_values()





