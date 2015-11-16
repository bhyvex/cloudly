# -*- coding: utf-8
#!/usr/bin/env python

import os
import time
import tweepy
import django

import json
from bson.objectid import ObjectId
from bson.json_util import dumps

import django
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudly.settings")
django.setup()

from pprint import pprint

from userprofile.models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

try:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)
except: pass

mongo = client.cloudly

active_service_statuses = mongo.active_service_statuses
historical_service_statuses = mongo.historical_service_statuses
alertor_queue = mongo.alertor_queue


if __name__ == "__main__":

    print "alertor started"

    while True:

        alert = alertor_queue.find_one_and_delete({})

        if(alert):

            alert_subject = alert['server_id'] + ' ' + alert['service'] + ' ' + alert['current_overall_status']
            alert_message = alert['detailed_service_status']['message'] + ':\n'
            alert_message += dumps(alert)

            user = Profile.objects.get(secret=alert["secret"])
            user_email = user.user.email

            send_mail(alert_subject,alert_message,'alertor@projectcloudly.org',[user_email,], fail_silently=True)

        time.sleep(0.1)
        print 'waiting for the q..'

    print 'ze end.'
