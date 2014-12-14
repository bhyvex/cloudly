#!/bin/sh
cp -rf cloudly/settings.py-server cloudly/settings.py
python2.7 manage.py runfcgi daemonize=false method=threaded host=127.0.0.1 port=8080 pidfile=/var/run/projectcloudly.pid --settings=cloudly.settings


