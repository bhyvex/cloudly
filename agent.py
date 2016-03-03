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

AGENT_VERSION = "0.7.5"
AGENT_ALLOWED_TO_SELFUPDATE = False
AGENT_PATH = "/opt/monitoring-agent.py"

REFRESH_INTERVAL = 2 # in seconds

SECRET = "" # to be injected on download by Cloudly
if(not SECRET): SECRET = raw_input("Enter your secret: ")

API_SERVER = "" # to be injected on download by Cloudly
if(not API_SERVER): API_SERVER = "127.0.0.1:5001"

os.environ["LANG"] = "POSIX"

if(not getpass.getuser()=="root"):
    print "You must be root to run this script."
    sys.exit(0)


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

    try:
        import json
        # old versions of python such as python 2.5.1 do not come with json nor they have support for one..
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


def self_update( secret ):

    print 'Running agent-self update..'

    conn = httplib.HTTPSConnection("raw.githubusercontent.com")
    conn.request( "GET", "/ProjectCloudly/cloudly/master/agent.py" )
    r1 = conn.getresponse()
    data = r1.read()

    print 'Downloading the new monitoring agent... OK'

    agent_code = ""
    for line in data.split('\n'):
        if("SECRET = \"\"" in line):
            agent_code += "SECRET = \""+secret+"\"\n"
            continue
        if("API_SERVER = \"\"" in line):
            agent_code += "API_SERVER = \""+API_SERVER+"\"\n"
            continue
        if("AGENT_ALLOWED_TO_SELF_UPDATE = \"\"" in line):
            agent_code += "AGENT_ALLOWED_TO_SELF_UPDATE = True\n"
            continue
        agent_code += line + "\n"

    print 'Saving the resultant monitoring agent code.. OK'

    f = open(AGENT_PATH, "w")
    f.write( agent_code )
    f.close()

    print 'Setting the agent file permissions.. OK'
    os.chmod(AGENT_PATH,0755)

    print 'Kicking off self update...'
    python = sys.executable
    os.execl(python, python, * sys.argv)

    return AGENT_VERSION


def _get_hostname():

    hostname = subprocess.Popen(["hostname"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    hostname = hostname.replace("\n","")
    return hostname


def _get_processes():

    processes = subprocess.Popen(["ps","a","u","x"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    return processes


def _get_sys_uptime():

    uptime = subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    uptime = re.findall("[ 0-9:]up[ ](.*)[,][ 0-9]+user", uptime)[0]

    return uptime


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


def _get_sys_cpu_virtualization():

    virtualization_support = False

    cpuinfo = open('/proc/cpuinfo','rt').readlines()
    for line in cpuinfo:

        if("vmx" in line):
            virtualization_support = True
        if("svm" in line):
            virtualization_support = True

    return virtualization_support


def _get_sys_cpu():

    cpu_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 70,
            'max_value': 90,
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

    cpu_total = float(0)
    cpu_info = subprocess.Popen(["ps","axo","pcpu"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

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
    elif(float(cpu_usage['cpu_used']) >= cpu_thresholds['WARNING']['min_value'] and float(cpu_usage['cpu_used']) <= cpu_thresholds['WARNING']['max_value']):
        status = 'WARNING'
    else:
        status = 'CRITICAL'

    message = 'The CPU(s) are '
    if(status == 'OK'): message = message + 'within limits'
    if(status == 'WARNING' or status == 'CRITICAL'):
        message = message + 'quite heavily utilized'

    service_status['status'] = status
    service_status['message'] = message
    service_status['values'] = cpu_usage

    service_report = {}
    service_report['service_thresholds'] = cpu_thresholds
    service_report['service_status'] = service_status

    return cpu_usage, service_report


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

    loadavg =subprocess.Popen(['uptime',], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    loadavg_ = re.findall(r"(\d+\.\d{2})", loadavg)

    try:
        float(loadavg_[2])
        loadavg = loadavg_
    except:

        count = 0
        loadavg = re.findall(r"(\d+\,\d{2})", loadavg)

        for i in loadavg:
            loadavg[count] = i.replace(',','.')
            count += 1


    status = 'UNKNOWN'

    if(float(loadavg[2]) < loadavg_thresholds['WARNING']['min_value']):
        status = 'OK'
    elif(float(loadavg[2]) >= loadavg_thresholds['WARNING']['min_value'] and float(loadavg[2]) <= loadavg_thresholds['WARNING']['max_value']):
        status = 'WARNING'
    else:
        status = 'CRITICAL'

    message = 'The System Load is'
    if(status == 'OK'): message = message + ' within limits'
    if(status == 'WARNING'): message = message + ' too high'
    if(status == 'CRITICAL'): message = message + ' ' + status

    loadavg_values = {
        "1-min":loadavg[0],
        "5-min":loadavg[1],
        "15-min":loadavg[2],
    }

    service_status['status'] = status
    service_status['message'] = message
    service_status['values'] = loadavg_values

    service_report = {}
    service_report['service_thresholds'] = loadavg_thresholds
    service_report['service_status'] = service_status

    return loadavg, service_report


def _get_memory_usage():

    memory_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 80, # mem used in percentage
            'max_value': 90, # mem used in percentage
            'min_duration_in_seconds': 60,
        },
        "CRITICAL": { # is everything above the warning range
            'min_duration_in_seconds': 120,
        },
    }
    service_status = {
        'status': '',
        'service': 'system_memory',
    }

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

    status = 'UNKNOWN'
    message = ''

    if(long(memory_usage['swap_used'])>0):
        status = 'WARNING'
        message = 'Swap memory is being utilized'

    if(long(memory_usage['swap_used_percentage'])>90):
        status = 'CRITICAL'
        message = 'Memory and the swap space is running out'

    if(status=='UNKNOWN'):
        if(float(memory_usage['memory_used_percentage']) < memory_thresholds['WARNING']['min_value']):
            status = 'OK'
            message = 'The Memory is within limits'
        elif(float(memory_usage['memory_used_percentage']) >= memory_thresholds['WARNING']['min_value'] and float(memory_usage['memory_used_percentage']) <= memory_thresholds['WARNING']['max_value']):
            status = 'WARNING'
            message = 'Server Memory is running out'
        else:
            status = 'CRITICAL'
            message = 'The system has ran out of memory'

    service_status['status'] = status
    service_status['message'] = message
    service_status['values'] = memory_usage

    service_report = {}
    service_report['service_thresholds'] = memory_thresholds
    service_report['service_status'] = service_status

    return memory_usage, service_report

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


def _get_disks_usage():

    disks_thresholds = {
        "OK": {},
        "WARNING": {
            'min_value': 90, # disk used in percentage
            'max_value': 95, # disk used in percentage
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


    disks_usage_  = []
    for disk in disks_usage:
        if(disk[0]=="udev" or disk[0]=="rmpfs" or disk[0]=="cgmfs" or disk[0]=="tmpfs"):
            continue
        disks_usage_.append(disk)
    disks_usage = disks_usage_

    overall_status = "UNKNOWN"
    messages = []
    disks_values = []


    for disk in disks_usage:

        status = 'UNKNOWN'

        mount_point = disk[5]
        disk_free = disk[3]
        disk_used = disk[2]
        disk_total = disk[1]
        #disk_usage = disk[4]

        if(int(disk[4].replace('%','')) < disks_thresholds['WARNING']['min_value']):
            status = 'OK'
        elif(int(disk[4].replace('%','')) >= disks_thresholds['WARNING']['min_value'] and int(disk[4].replace('%','')) <= disks_thresholds['WARNING']['max_value']):
            status = 'WARNING'
            if(overall_status!="CRITICAL"): overall_status = "WARNING"
        else:
            status = 'CRITICAL'
            overall_status = "CRITICAL"

        if(overall_status != 'WARNING' and overall_status != 'CRITICAL'): overall_status = "OK"

        message = 'The disk "' + disk[-1:][0] + '"'

        if(status == 'WARNING' or status == 'CRITICAL'):
            message = 'Warning - ' + message + ' is running out of space'
        if(status == 'OK'):
            message += ' is within limits'

        disk_values = {}
        disk_values['disk_free'] = disk_free
        disk_values['disk_used'] = disk_used
        disk_values['disk_total'] = disk_total

        messages.append(message)
        disks_values.append(disk_values)

    service_status['status'] = overall_status
    service_status['messages'] = messages
    service_status['values'] = disks_values

    service_report = {}
    service_report['service_thresholds'] = disks_thresholds
    service_report['service_status'] = service_status

    return disks_usage, service_report

def _get_networking_stats():

    try:
        proc = subprocess.Popen(['/sbin/iptables','-L','-vxn'], stdout=subprocess.PIPE, close_fds=True)
    except:
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
    input_accept_packets = 0
    input_accept_bytes = 0

    for line in inbound_text.split('\n'):

        if("INPUT" in line):
            input_accept = line.split('policy ACCEPT ')[1]
            input_accept = input_accept.split(' ')
            input_accept_packets = input_accept[0]
            input_accept_bytes = input_accept[2]
            break

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
    output_accept_packets = 0
    output_accept_bytes = 0

    for line in outbound_text.split('\n'):

        if("OUTPUT" in line):
            output_accept = line.split('policy ACCEPT ')[1]
            output_accept = output_accept.split(' ')
            output_accept_packets = output_accept[0]
            output_accept_bytes = output_accept[2]
            break

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

    try:
        proc = subprocess.Popen(['/sbin/iptables','-Z'], stdout=subprocess.PIPE, close_fds=True)
    except:
        proc = subprocess.Popen(['iptables','-Z'], stdout=subprocess.PIPE, close_fds=True)

    return networking


def _get_network_connections():

    try:
        netstat = subprocess.Popen(["/bin/netstat","-atn"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    except:
        netstat = subprocess.Popen(["/usr/sbin/netstat","-atn"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    connections = {}
    listen_connections = []
    established_connections = []

    for line in netstat.split('\n'):

        if("tcp" in line or "udp" in line):

            line = re.split(" +", line)

            proto = line[0]
            recvq = line[1]
            sendq = line[2]
            local_address = line[3]
            foreign_address = line[4]
            state = line[5]

            local_address_port = local_address.split(':')[-1:][0]
            foreign_address_port = foreign_address.split(':')[-1:][0]

            local_address_port_resolved = ""
            foreign_address_port_resolved = ""

            if(local_address_port!="*"):
                try:
                    local_address_port_resolved = socket.getservbyport(int(local_address_port))
                except: pass

            if(foreign_address_port!="*"):
                try:
                    foreign_address_port_resolved = socket.getservbyport(int(foreign_address_port))
                except: pass

            if(state=="LISTEN"):
                listen_connections.append([state, proto, recvq, sendq, local_address, local_address_port, local_address_port_resolved, foreign_address, foreign_address_port, foreign_address_port_resolved] )
                #print state, proto, recvq, sendq, local_address, local_address_port, local_address_port_resolved, foreign_address, foreign_address_port, foreign_address_port_resolved

            if(state=="ESTABLISHED"):
                established_connections.append([state, proto, recvq, sendq, local_address, local_address_port, local_address_port_resolved, foreign_address, foreign_address_port, foreign_address_port_resolved] )
                #print state, proto, recvq, sendq, local_address, local_address_port, local_address_port_resolved, foreign_address, foreign_address_port, foreign_address_port_resolved

    connections['listen'] = listen_connections
    connections['established'] = established_connections
    connections['description'] = "Active Internet Connections (including servers)"

    return connections


def _get_distro():

    distro = ""
    try:
        for i in platform.linux_distribution():
            distro += i.title() + " "
        distro = distro[:-1]
    except: distro = "?"

    return distro


def send_data( secret, api_call, data ):

    try:
        import json
    except:
        try:
            import simplejson as json
        except: pass

    params = urllib.urlencode(data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # fixing codacy duplication analysis
    params = params

    #api_url = "http://"+API_SERVER+api_call

    while True:

        print datetime.datetime.now(), 'Querying API server ' + API_SERVER + ' ..'
        try:
            conn = httplib.HTTPConnection(API_SERVER)
            conn.request("POST", api_call, json.dumps(data), headers)
            response = conn.getresponse()
            response_data = response.read()
            conn.close()
            break
        except:
            print 'Connection Error. Retrying in 2 seconds..'
            time.sleep(2)

    return response_data


def get_system_metrics( uuid, secret ):

    uuid = uuid
    ip = _get_ip_address()
    distro = _get_distro()
    uptime = _get_sys_uptime()
    hostname = _get_hostname()
    cpu_info = _get_sys_cpu_info()
    cpu_virtualization = _get_sys_cpu_virtualization()

    loadavg = {}
    loadavg_data, loadavg_service_report = _get_sys_loadavg()
    loadavg['loadavg'] = loadavg_data
    loadavg['service_report'] = loadavg_service_report

    cpu_usage = {}
    cpu_usage_data, cpu_usage_service_report = _get_sys_cpu()
    cpu_usage['cpu_usage'] = cpu_usage_data
    cpu_usage['service_report'] = cpu_usage_service_report

    memory_usage = {}
    memory_usage_data, memory_usage_service_report = _get_memory_usage()
    memory_usage['memory_usage'] = memory_usage_data
    memory_usage['service_report'] = memory_usage_service_report

    disks_usage = {}
    disks_usage_data, disks_usage_service_report = _get_disks_usage()
    disks_usage['disks_usage'] = disks_usage_data
    disks_usage['service_report'] = disks_usage_service_report

    processes = _get_processes()
    networking = _get_networking_stats()
    network_connections = _get_network_connections()

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
        'network_connections': network_connections,
        'agent_version': AGENT_VERSION,
    }

    print datetime.datetime.now(), 'Successfully collected system metrics..'

    return system_metrics_json


def main():

    setup_system()

    print "AGENT: v"+AGENT_VERSION
    print "Written By: Jan Paricka"

    try:
        HWADDR = subprocess.Popen(["/sbin/ifconfig","-a"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    except:
        HWADDR = subprocess.Popen(["ifconfig","-a"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]

    UUID = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', HWADDR, re.I).group()

    api_call = "/v10/activity/"
    activity = {
        'secret': SECRET,
        'server_id': UUID,
        'activity_type': "AGENT_STARTED",
        'data': {
            "agent_version": AGENT_VERSION,
            "message": "Agent v"+AGENT_VERSION+" started.",
            }
        }
    send_data(SECRET,api_call,activity)

    while True:

        api_call = "/v10/ping/"
        system_metrics = get_system_metrics(UUID, SECRET)
        api_response = send_data(SECRET,api_call,system_metrics)

        if(api_response=="update" and AGENT_ALLOWED_TO_SELFUPDATE):

            api_call = "/v10/activity/"
            activity = {
                'secret': SECRET,
                'server_id': UUID,
                'activity_type': "AGENT_UPDATED",
                'data': {
                    "agent_version": AGENT_VERSION,
                    "message": "Agent self-updated to the latest version.",
                    }
                }
            send_data(SECRET,api_call,activity)
            self_update(SECRET)


        if(api_response=="stop"):

            api_call = "/v10/activity/"
            activity = {
                'secret': SECRET,
                'server_id': UUID,
                'activity_type': "AGENT_STOPPED",
                'data': {
                    "agent_version": AGENT_VERSION,
                    "message": "API issued stop command. Agent stopped.",
                    }
                }
            send_data(SECRET,api_call,activity)
            self_update(SECRET)

            print "API issued stop command. Exiting.."
            sys.exit(0)


        time.sleep(REFRESH_INTERVAL)

    print "ze end."


if __name__=="__main__":

    main()
