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


def _get_network_sessions():

    print 'Active Internet Connections (including servers)'
    
    # XXX resolve services

    try:
        netstat = subprocess.Popen(["/bin/netstat","-atn"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]
    except:
        netstat = subprocess.Popen(["/usr/sbin/netstat","-atn"], stdout=subprocess.PIPE, close_fds=True).communicate()[0]


    for line in netstat.split('\n'):
    
        if("tcp4" in line or "udp4" in line):

            line = re.split(" +", line)

            proto = line[0]
            recvq = line[1]
            sendq = line[2]
            local_address = line[3]
            foreign_address = line[4]
            state = line[5]
    
            if(state):
            
                print state, recvq, sendq, local_address, foreign_address


    
    return "XXX"
    
    
    
_get_network_sessions()

    
