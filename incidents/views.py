# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

from django.shortcuts import render_to_response
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

    print '-- incidents:', request.user

    user = request.user
    profile = Profile.objects.get(user=request.user)
    secret = profile.secret

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/incidents/","incidents",ip=ip)

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    servers = mongo.servers.find({'secret':profile.secret},{'uuid':1,'name':1}).sort('_id',-1);

    serversNames = {}
    for server in servers:
        serversNames[server['uuid']] = server['name']

    active_service_statuses = mongo.active_service_statuses

    active_notifs = {}
    notifs_types = ["CRITICAL","WARNING","UNKNOWN",]
    for notifs_type in notifs_types:
        active_notifs[notifs_type] = []
        notifs = active_service_statuses.find({"secret":secret,"current_overall_status":notifs_type})
        for notif in notifs:
            notif.update({'name':serversNames[notif['server_id']]})

            server = mongo.servers.find_one({'uuid':notif['server_id'],})
            if((datetime.datetime.now()-server['last_seen']).total_seconds()<20):
                active_notifs[notifs_type].append(notif)


    return render_to_response(
        'incidents.html',
        {
            'request':request,
            'secret':profile.secret,
            'active_notifs':active_notifs
        },
        context_instance=RequestContext(request),
    )


@login_required
def logs(request):

    print '-- system logs:', request.user

    user = request.user
    profile = Profile.objects.get(user=request.user)
    secret = profile.secret

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/logs/","logs",ip=ip)

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    servers = mongo.servers.find({'secret':secret,})
    activities = mongo.activity.find({'secret':secret,}).sort("_id",pymongo.DESCENDING)
    activities = activities.limit(20)

    servers_ = mongo.servers.find({'secret':profile.secret},{'uuid':1,'name':1}).sort('_id',-1);

    serversNames = {}
    for server in servers_:
        serversNames[server['uuid']] = server['name']

    active_service_statuses = mongo.active_service_statuses

    active_notifs = {}
    notifs_types = ["CRITICAL","WARNING","UNKNOWN",]

    for notifs_type in notifs_types:

        active_notifs[notifs_type] = []
        notifs = active_service_statuses.find({"secret":secret,"current_overall_status":notifs_type})
        for notif in notifs:
            notif.update({'name':serversNames[notif['server_id']]})

            server = mongo.servers.find_one({'uuid':notif['server_id'],})
            if((datetime.datetime.now()-server['last_seen']).total_seconds()<20):
                active_notifs[notifs_type].append(notif)

    # XXX test for offline servers
    offline_servers = []
    for server in mongo.servers.find({"secret":profile.secret,}):
        if((datetime.datetime.now()-server['last_seen']).total_seconds()>300):
            offline_servers.append(server)

    return render_to_response(
        'logs.html',
        {
            'request':request,
            'secret':profile.secret,
            'servers':servers,
            'offline_servers':offline_servers,
            'activities':activities,
            'active_notifs':active_notifs
        },
        context_instance=RequestContext(request),
    )
