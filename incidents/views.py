# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch

from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.views import _log_user_activity
from django.contrib.auth.decorators import login_required

from django.conf import settings

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

if settings.MONGO_USER:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)

mongo = client.cloudly

@login_required()
def incidents(request):

    print '-- system logs:', request.user

    user = request.user
    profile = Profile.objects.get(user=request.user)
    secret = profile.secret

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/logs/","logs",ip=ip)

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    notifs_counter = 0
    active_service_statuses = mongo.active_service_statuses
    active_service_statuses_data = active_service_statuses.find({"$and": [{"secret": secret}, {"current_overall_status": {"$ne": "OK"}}]})
    notifs_counter = active_service_statuses_data.count()

    unknown_notifs = active_service_statuses.find({"secret":secret,"current_overall_status":"UNKNOWN"})
    warning_notifs = active_service_statuses.find({"secret":secret,"current_overall_status":"WARNING"})
    critical_notifs = active_service_statuses.find({"secret":secret,"current_overall_status":"CRITICAL"})

    return render_to_response('incidents.html', {'request':request,'notifs_counter':notifs_counter,'active_service_statuses':active_service_statuses_data,'unknown_notifs':unknown_notifs,'warning_notifs':warning_notifs,'critical_notifs':critical_notifs,'profile':profile,}, context_instance=RequestContext(request))
