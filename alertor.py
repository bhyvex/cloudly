#!/usr/bin/env python
# -*- coding: utf-8

import os
import time
import tweepy
import django
import datetime

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

servers = mongo.servers
servers_active_availibility = mongo.servers_active_availibility
servers_historical_availibility = mongo.servers_historical_availibility

alertor_queue = mongo.alertor_queue

auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

OFFLINE_SERVER_THRESHOLD = 300
FORCE_TWEETS_FOR_TESTING = False

def _file_activity( activity_data ):

    activity_log = {
        'secret': activity_data['secret'],
        'server_id': activity_data['server_id'],
        'activity_type': activity_data['activity_type'],
        'data': activity_data['data'],
        'date_created': datetime.datetime.now(),
    }
    activity_ = mongo.activity
    activity_.insert( activity_log )

    # XXX file historical activity

    return True


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
            user_secret = alert['secret']

            # XXX consider obsessive chasing profile settings here
            send_mail( \
                subject = alert_subject,
                message = alert_message,
                html_message = alert_html_message,
                from_email = 'alertor@projectcloudly.org',
                recipient_list = [user_email],
                fail_silently=True
                )
            activity_data = {
                'secret': user_secret,
                'server_id': server_id,
                'activity_type': 'EMAIL_SENT',
                'data': {
                    "subject": alert_subject,
                    "message": alert_message,
                    "html_message": alert_html_message,
                    "from_email": 'alertor@projectcloudly.org',
                    "recipient_list": [user_email],
                },
            }
            _file_activity( activity_data )

            if(not settings.DEBUG or FORCE_TWEETS_FOR_TESTING):

                # XXX we need a way to define twitter info for ones' account, i.e. @jaricka in there is temporary....

                # XXX consider obsessive chasing profile settings here
                twitter_api.update_status(status='@jparicka '+alert_subject)
                activity_data = {
                    'activity_type': 'TWEET_SENT',
                    'data': { 'tweet': alert_subject },
                }
                _file_activity( activity_data )


        print 'looking up offline servers..'
        offline_servers = servers.find({"last_seen": {"$lte":datetime.datetime.now()-datetime.timedelta(seconds=OFFLINE_SERVER_THRESHOLD)}})

        if(offline_servers):

            print 'offline_servers', offline_servers.count()
            print 'XXX work offline_servers schema / logic for tracking server offline/online emails..'
            print 'XXX file an activity on when the server is registered and has gone offline..'
            print 'XXX remember to work the historical servers availibility'
            print 'XXX send out actual notifs'

        # XXX
        print 'XXX loop through active offline servers to update check their statuses'

        print 'alertor: waiting for new alerts..'
        if(settings.DEBUG): time.sleep(1)
        time.sleep(0.1)


    print 'ze end.'
