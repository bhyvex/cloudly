# -*- coding: utf-8
#!/usr/bin/env python

import os
import sys
import re
import time
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

AGENT_VERSION = "0.1"

SECRET = "" # to be injected on download by Cloudly
if(not SECRET): SECRET = raw_input("Enter your secret: ")

API_SERVER = "" # to be injected on download by Cloudly
if(not API_SERVER): API_SERVER = "127.0.0.1:5001"


if(not getpass.getuser()=="root"):
    print "You must be root to run this script."
    sys.exit(0)


def _get_sys_loadavg():

    threshold_values = {
        "5-mins":None,
        "10-mins":None,
        "15-mins":None,
    }
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


def _get_sys_cpu_info():

    cpu = 0
    cpu_info = {}

    for line in open('/proc/cpuinfo').readlines():

        element = re.findall(r"^(.+)\s+[:][ ](.*)$", line)

        if(element):

            key = element[0][0].replace('\t','').replace(' ','_')
            value = element[0][1]

            try:
                cpu_info['cpu'+str(cpu)][key] = value
            except:
                cpu_info['cpu'+str(cpu)] = {}
                cpu_info['cpu'+str(cpu)][key] = value

        if(len(line)==1): cpu += 1

    return cpu_info


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


def _get_ip_address():
    
    try:
        ifconfig = subprocess.Popen(["/sbin/ifconfig","-a"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    except:
        ifconfig = subprocess.Popen(["ifconfig","-a"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    
    ip = re.search( r'inet addr:[^\s]+', ifconfig )
    
    if(not ip):
        ip = re.search( r'inet [^\s]+', ifconfig )
    
    if not platform.system() == 'Darwin':
        ip = ip.group().split(':')[-1]
    else:
        ip = "127.0.0.1"
        
    ip = ip.replace(" ","")
    ip = ip.replace("inet","")
    
    return ip
    

def _get_sys_cpu_virtualization():

    virtualization_support = False

    cpuinfo = open('/proc/cpuinfo','rt').readlines()
    for line in cpuinfo:
        
        if("vmx" in line): 
            virtualization_support = True
        if("svm" in line): 
            virtualization_support = True
        
    return virtualization_support


def _get_disks_usage():

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
    
    return disks_usage


def _get_networking_stats():

    proc = subprocess.Popen(['iptables','-L','-vxn'], stdout=subprocess.PIPE, close_fds=True)
    data = proc.communicate()[0]
    
    inbound_text = ""
    outbound_text = ""
    forward_text = ""
    
    psc = 0
    for line in data.split('\n'):

        if(psc==0):
            if(line): inbound_text += line+"\n"
        if(psc==1):
            if(line): forward_text += line+"\n"
        if(psc==2):
            if(line): outbound_text += line+"\n"

        if(len(line)==0): psc += 1


    inbound_traffic = {}

    for line in inbound_text.split('\n'):

        if("INPUT" in line):
            input_accept = line.split('policy ACCEPT ')[1]
            input_accept = input_accept.split(' ')
            input_accept_packets = input_accept[0]
            input_accept_bytes = input_accept[2]
            break


    inbound_traffic['input_accept_packets'] = input_accept_packets
    inbound_traffic['input_accept_bytes'] = input_accept_bytes

    input_accept_packets = 0
    input_accept_bytes = 0

    if(len(inbound_text.split('\n'))>3):

        c=0
        for line in inbound_text.split('\n'):
            
            if(c>3 and c<len(inbound_text.split('\n'))-1):
                input_accept_packets += int(line.split(' ')[0])
                input_accept_bytes += int(line.split(' ')[1])
                
            c+=1

    if(input_accept_packets>0): inbound_traffic['input_accept_packets'] = input_accept_packets
    if(input_accept_bytes>0): inbound_traffic['input_accept_bytes'] = input_accept_bytes


    outbound_traffic = {}

    for line in outbound_text.split('\n'):
    
        if("OUTPUT" in line):
            output_accept = line.split('policy ACCEPT ')[1]
            output_accept = output_accept.split(' ')
            output_accept_packets = output_accept[0]
            output_accept_bytes = output_accept[2]
            break

    outbound_traffic['output_accept_packets'] = output_accept_packets
    outbound_traffic['output_accept_bytes'] = output_accept_bytes

    output_accept_packets = 0
    output_accept_bytes = 0

    if(len(outbound_text.split('\n'))>3):

        c=0
        for line in outbound_text.split('\n'):
            
            if(c>3 and c<len(outbound_text.split('\n'))-1):
                output_accept_packets += int(line.split(' ')[0])
                output_accept_bytes += int(line.split(' ')[1])
                
            c+=1

    if(output_accept_packets>0): outbound_traffic['output_accept_packets'] = output_accept_packets
    if(output_accept_bytes>0): outbound_traffic['output_accept_bytes'] = output_accept_bytes

    networking = {'input_accept_packets':inbound_traffic['input_accept_packets'],'input_accept_bytes':inbound_traffic['input_accept_bytes'],'output_accept_packets':outbound_traffic['output_accept_packets'],'output_accept_bytes':outbound_traffic['output_accept_bytes'],}
    proc = subprocess.Popen(['iptables','-Z'], stdout=subprocess.PIPE, close_fds=True)

    return networking


def _get_distro():

    distro = "?"
    try:
        for i in platform.linux_distribution(): 
            distro += i.title() + " "
        distro = distro[:-1]

    except: pass

    return distro
    

def _get_hostname():
    
    hostname = subprocess.Popen(["hostname"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    hostname = hostname.replace("\n","")
    return hostname

def _get_processes():

    processes = subprocess.Popen(["ps","a","u","x"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    return processes
    
    
# XXX
# class nginx
# class mysql
# class mwah

def get_system_metrics( uuid, secret ):

    print datetime.datetime.now(), 'Collecting system metrics..'

    uuid = uuid
    ip = _get_ip_address()
    distro = _get_distro()
    loadavg = _get_sys_loadavg()
    uptime = _get_sys_uptime()
    cpu_usage = _get_sys_cpu()
    cpu_info = _get_sys_cpu_info()
    cpu_virtualization = _get_sys_cpu_virtualization()
    memory_usage = _get_memory_usage()
    disks_usage = _get_disks_usage()
    processes = _get_processes()
    hostname = _get_hostname()
    networking = _get_networking_stats()
    
    system_metrics_json = {
        'uuid': uuid,
        'ip': ip,
        'hostname': hostname,
        'distro': distro,
        'secret': secret,
        'loadavg': loadavg,
        'uptime': uptime,
        'cpu_usage': cpu_usage,
        'cpu_info': cpu_info,
        'cpu_virtualization': cpu_virtualization,
        'memory_usage': memory_usage,
        'disks_usage': disks_usage,
        'processes': processes,
        'networking': networking,
        'agent_version': AGENT_VERSION,
    }

    return system_metrics_json


def send_data( secret, api_call, data ):
    
    params = urllib.urlencode(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    api_url = "http://"+API_SERVER+api_call
            
    conn = httplib.HTTPConnection(API_SERVER)
    conn.request("POST", api_call, json.dumps(data), headers)
    response = conn.getresponse()
    response_data = response.read()
    conn.close()
    
    return response_data
    

def setup_system():

    installer = ""

    proc = subprocess.Popen(['which','yum'], stdout=subprocess.PIPE, close_fds=True)
    proc = proc.communicate()[0]
    if('yum' in proc): installer = proc

    if(not installer):
                    
        proc = subprocess.Popen(['which','apt-get'], stdout=subprocess.PIPE, close_fds=True)
        proc = proc.communicate()[0]
        if('apt-get' in proc): installer = proc

    if(not installer):
    
        proc = subprocess.Popen(['which','emerge'], stdout=subprocess.PIPE, close_fds=True)
        proc = proc.communicate()[0]
        if('emerge' in proc): installer = proc
    

    if(not installer):
    
        proc = subprocess.Popen(['which','zypper'], stdout=subprocess.PIPE, close_fds=True)
        proc = proc.communicate()[0]
        if('zypper' in proc): installer = proc
        
    installer = installer.replace('\n','')


    # iptables..

    proc = subprocess.Popen(['which','iptables'], stdout=subprocess.PIPE, close_fds=True)
    proc = proc.communicate()[0]

    if(not 'iptables' in proc):

        print 'Installing iptables..'

        if(not installer):
            print 'Please install the iptables and re-run the agent.'
            sys.exit(0)

        if("emerge" in installer):
            os.system(installer+" iptables") # there is no install param in emerge
        else:
            os.system(installer+" install iptables")
    

    
    # old versions of python such as python 2.5.1 do not come with json nor they have support for one..

    try:
    
        import json
        
    except: 
    
        try:
            
            import simplejson as json
                    
        except:
    
            print 'Installing python-simplejson..'
        
            if(not installer):
                print 'Please install the python-simplejson and re-run the agent.'
                sys.exit(0)

            if("emerge" in installer):
                os.system(installer+" python-simplejson") # there is no install param in emerge
            else:
                os.system(installer+" install python-simplejson")       
    
    return True
    

def main():

    setup_system()
    os.system("clear")
        
    print "AGENT: v"+AGENT_VERSION
    print "Written By: Jan Paricka"
    
    HWADDR = subprocess.Popen(["ifconfig","-a"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    UUID = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', HWADDR, re.I).group()

    api_call = "/v10/activity/"
    activity = {
        'secret': SECRET,
        'agent_version': AGENT_VERSION,
        'uuid': UUID,
        'activity': "Agent v"+AGENT_VERSION+" started."
    }
    send_data(SECRET,api_call,activity)
    
    while True:
    
        api_call = "/v10/ping/"
        system_metrics = get_system_metrics(UUID, SECRET)
        api_response = send_data(SECRET,api_call,system_metrics)
        time.sleep(2)

    print "ze end."


if __name__=="__main__":

    main()
