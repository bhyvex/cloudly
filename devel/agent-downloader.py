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


def self_update():

    conn = httplib.HTTPSConnection("raw.githubusercontent.com")
    conn.request( "GET", "/jparicka/cloudly/master/agent.py" )
    r1 = conn.getresponse()
    data = r1.read()

    print data

    return AGENT_VERSION
    

print self_update()

