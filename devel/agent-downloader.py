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

    agent_url = "https://raw.githubusercontent.com/jparicka/cloudly/master/agent.py"


    return AGENT_VERSION
    

print self_update()

