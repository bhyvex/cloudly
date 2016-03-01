# -*- coding: utf-8 -*-

import os
import time
import logging
import base64, pickle
import datetime

from django.db.models import Q

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch

from vms.models import Cache

from django.contrib.auth.models import User
from userprofile.models import Profile, Activity

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
def devel(request):

    print '-'*1000
    request.session['x'] = True
    request.session.modified = True

    print request.session.keys()

    return render_to_response('devel.html', {'request':request,}, context_instance=RequestContext(request))


@login_required()
def user_activity_report(request, user_id):

    print '-- admin report user activity', user_id

    if not request.user.is_staff:
        return HttpResponseRedirect("/")

    print request.user

    profile = Profile.objects.get(user=request.user)

    u = User.objects.get(pk=user_id)

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/admin/user/"+str(user_id)+"/report/","user_activity_report",ip=ip)

    user_activity = Activity.objects.filter(user=u).order_by('-pk')
    user_activity_clicks = Activity.objects.filter(user=u,activity="click").order_by('-pk')
    user_activity_other = Activity.objects.filter(user=u).filter(~Q(activity="click")).order_by('-pk')

    user_profile = Profile.objects.get(user=u)

    try:
        vms_cache = Cache.objects.get(user=u)
        vms_response = vms_cache.vms_response
        vms_response = base64.b64decode(vms_response)
        vms_response = pickle.loads(vms_response)
        vms_cached_response = vms_response
        #vms_cached_response['last_seen'] = vms_cache.last_seen
    except: vms_cached_response = None


    servers = mongo.servers.find({'secret':user_profile.secret,}).sort('_id',-1)

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    return render_to_response('admin_user_report.html', {'u':u,'vms_cached_response':vms_cached_response,'user_profile':user_profile,'user_files':[],'user_activity':user_activity,'user_activity_clicks':user_activity_clicks,'user_activity_other':user_activity_other,'profile':profile,'servers':servers,}, context_instance=RequestContext(request))


@login_required()
def admin(request):

    print '--  admin page:'

    if not request.user.is_staff:
        return HttpResponseRedirect("/")

    print request.user

    users = Profile.objects.all().order_by('-last_seen')
    profile = Profile.objects.get(user=request.user)

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    users = Profile.objects.all().order_by('-pk')

    ip = request.META['REMOTE_ADDR']
    _log_user_activity(profile,"click","/admin/","admin",ip=ip)

    return render_to_response('admin.html', {'users':users,'files':[],'profile':profile,'request':request,}, context_instance=RequestContext(request))
