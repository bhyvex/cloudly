# -*- coding: utf-8
#!/usr/bin/env python

import os
import time
import tweepy
import json
import django

import django
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudly.settings")
django.setup()

from userprofile.models import Profile
from django.contrib.auth.models import User


import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

try:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)
except: pass

mongo = client.cloudly


if __name__ == "__main__":

    print "alertor started"

    print '.'
