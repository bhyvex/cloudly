#!/usr/bin/env python
# -*- coding: utf-8

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

from api import activity as file_activity

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

try:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)
except: pass

mongo = client.cloudly

servers = mongo.servers
active_service_statuses = mongo.active_service_statuses
historical_service_statuses = mongo.historical_service_statuses
alertor_queue = mongo.alertor_queue

auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)


if __name__ == "__main__":

    print "alertor started"

    while True:

        alert = alertor_queue.find_one_and_delete({})

        if(alert):

            server = servers.find_one({'secret':alert["secret"], 'uuid':alert['server_id'],})

            try:
                server_name = server['name']
            except:
                try:
                    server_name = server['hostname']
                except: server_name = alert['server_id']

            alert_subject = server_name + ' ' + alert['service'] + ' ' + alert['current_overall_status']
            alert_message = alert['detailed_service_status']['message'] + ':' + '\n'
            alert_message += dumps(alert)
            alert_html_message = "<html><body>"+alert_message+"</body></html>"

            user = Profile.objects.get(secret=alert["secret"])
            user_email = user.user.email

            send_mail( \
                subject = alert_subject,
                message = alert_message,
                html_message = alert_html_message,
                from_email = 'alertor@projectcloudly.org',
                recipient_list = [user_email],
                fail_silently=True
                )

            # XXX first we need a way to define twitter info for ones' account, i.e. @jaricka in there is temporary....
            twitter_api.update_status(status='@jparicka '+alert_subject)

            # XXX file an activity on behalf of the server agent....

        time.sleep(0.1)
        print 'alertor: waiting for the q..'

    print 'ze end.'
