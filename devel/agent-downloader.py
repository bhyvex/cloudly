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


AGENT_VERSION = "0.1"
AGENT_ALLOWED_TO_SELF_UPDATE = True
API_SERVER = "api.projectcloudly.com:5001"
AGENT_PATH = "/opt/monitoring-agent.py"

def self_update( uuid, secret ):

    conn = httplib.HTTPSConnection("raw.githubusercontent.com")
    conn.request( "GET", "/jparicka/cloudly/master/agent.py" )
    r1 = conn.getresponse()
    data = r1.read()

    agent_code = ""
    for line in data.split('\n'):
        if("SECRET = \"\"" in line):
            agent_code += "SECRET = \""+secret+"\"\n"
            continue
        if("API_SERVER = \"\"" in line):
            agent_code += "API_SERVER = \""+API_SERVER+"\"\n"
            continue
        agent_code += line + "\n"

    f = open(AGENT_PATH, "w")
    f.write( agent_code )
    f.close()

    return AGENT_VERSION
    

uuid = 'xxx'
secret = 'secret'

print self_update( uuid, secret )


