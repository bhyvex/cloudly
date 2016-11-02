# -*- coding: utf-8 -*-

import os
import time
import socket
import random
import logging
import datetime
import base64, pickle

import urllib2, json
from pprint import pprint

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity
from django.contrib.auth.decorators import login_required

from django.conf import settings

from amazon import ec2_funcs
from vms.models import Cache

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)

if settings.MONGO_USER:
    client.cloudly.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)

mongo = client.cloudly

CLOUDLY_MOTTOS = [
    "The Power of Now!",
    "Details Matters!",
    "Smart, Smarter, the Smartest",
    "Bulletproof monitoring out of the box.",
    "Save time and effort with our simple, reliable server monitoring.",
    "Get your servers into shape! 100% free for Open Source.",
    "The only Servers Monitoring that does the Heartbeats!",
    "Your Servers Heartbeat Visualised.",
    "Magical Servers Monitoring.",
    "Monitoring Solution for your Servers.",
    "Admins and DevOps love it!",
    "Relax, it's going to take no time!",
    "Saves you money and resources!",
    "Real-time servers monitoring.",
    "Real-time playful monitoring.",
    "Playful Servers Monitoring.",
    "Playful Servers Dashboard.",
    "Does the server monitoring for you.",
    "Cheerful Posix Servers Monitoring.",
    "Old School Servers Monitoring.",
    "Keeps a watchfull eye on your servers.",
    "The Coolest Servers Monitoring Out There!",
    "The Coolest Monitoring Out There!",
    "The Coolest Real-time Monitoring.",
    "The Ultimate Servers Monitoring.",
    "The Ultimate Dashboard for Your Servers.",
    "OpenTSDB Powered Servers Monitoring.",
    "The Ultimate Servers and Devices Monitoring.",
    "The Ultimate Servers Dashboard.",
    "The Ultimate Real-time Servers Monitoring.",
    "Dreamlike Servers Monitoring.",
    "Monitor Anything and Everything.",
    "Monitoring in the snap of a finger.",
    "Servers, And Apps Monitoring.",
    "Servers, Devices and Apps Monitoring.",
    "Hadoop Powered Servers Monitoring.",
    "Hadoop &amp; OpenTSDB Powered Servers Monitoring.",
    "The first line of defence for your servers.",
    "A free, open-source, cross-platform servers monitoring.",
    "Your servers visualized.",
]



def web_new_1(request):

    print '--  web 1:'
    random_motto = CLOUDLY_MOTTOS[ random.randint(0,len(CLOUDLY_MOTTOS)-1) ]
    return render_to_response('web1.html', {'random_motto':random_motto,},)

def web_new_2(request):

    print '--  web 2:'
    random_motto = CLOUDLY_MOTTOS[ random.randint(0,len(CLOUDLY_MOTTOS)-1) ]
    return render_to_response('web2.html', {'random_motto':random_motto,},)

def web_new_3(request):

    print '--  web 3:'
    random_motto = CLOUDLY_MOTTOS[ random.randint(0,len(CLOUDLY_MOTTOS)-1) ]
    return render_to_response('web.html', {'random_motto':random_motto,},)


def home(request):

    if not request.user.is_authenticated():
        print '--  web:'
        random_motto = CLOUDLY_MOTTOS[ random.randint(0,len(CLOUDLY_MOTTOS)-1) ]
        return render_to_response(
            'current-web.html',
            {'random_motto':random_motto,}
        )

    print '--  dashboard:'
    print request.user

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()

    profile = userprofile.objects.get(user=request.user)
    secret = profile.secret

    ip = request.META['REMOTE_ADDR']
    try:
        _log_user_activity(profile,"click","/","home",ip=ip)
    except: pass

    is_updating = False

    try:
        vms_cache = Cache.objects.get(user=request.user)
        vms_response = vms_cache.vms_response
        vms_response = base64.b64decode(vms_response)
        vms_response = pickle.loads(vms_response)
        vms_cached_response = vms_response
        vms_cached_response['last_seen'] = vms_cache.last_seen
        is_updating = vms_cache.is_updating
    except: vms_cached_response = None

    servers = mongo.servers.find({'secret':profile.secret,}).sort('_id',-1);
    servers_tags = {}

    for server in servers:
        if 'tags' in server:
            for tag_category in server['tags']:
                if(not servers_tags.has_key(tag_category)):
                    servers_tags[tag_category] = [];

                for inner_tag in server['tags'][tag_category]:
                    if(not inner_tag[0] in servers_tags[tag_category]):
                        servers_tags[tag_category].append(inner_tag[0])

    return render_to_response(
        'dashboard.html',
        {
            'servers_tags':servers_tags,
            'is_updating':is_updating,
            'vms_cached_response':vms_cached_response,
        },
        context_instance=RequestContext(request)
    )

@login_required()
def welcome(request):

    print '--  welcome page:', request.user

    ip = request.META['REMOTE_ADDR']
    profile = userprofile.objects.get(user=request.user)
    _log_user_activity(profile,"click","/welcome/","welcome",ip=ip)

    print request.user

    return render_to_response(
        'welcome.html',
        locals(),
        context_instance=RequestContext(request)
    )


def credits(request):

    try:
        print '--  credits page:', request.user
    except:
        print '--  credits page: anonymous'

    ip = request.META['REMOTE_ADDR']
    try:
        profile = userprofile.objects.get(user=request.user)
        _log_user_activity(profile,"click","/credits/","credits",ip=ip)
    except:
        return HttpResponseRedirect("/")


    print request.user

    return render_to_response('credits.html', {'request':request,}, context_instance=RequestContext(request))


def temp(request):

    try:
        print '--  temp page:', request.user
    except:
        print '--  temp page: anonymous'

    ip = request.META['REMOTE_ADDR']
    print request.user

    x = [1,2,3,4]

    return render_to_response('temp.html', {'request':request,'x':x,}, context_instance=RequestContext(request))


def support(request):

    try:
        print '-- support:', request.user
    except:
        print '-- support:'

    ip = request.META['REMOTE_ADDR']
    print request.user

    return render_to_response('support.html', {'request':request,}, context_instance=RequestContext(request))


def download_agent(request):

    print '-- download agent:'

    server_url = request.build_absolute_uri('/')
    api_server_url = server_url
    api_server_url = api_server_url.replace('http://','').replace('https://','')
    api_server_url = api_server_url.split(':')[0].replace('/','')
    api_server_url = api_server_url + ":5001"

    if('projectcloudly.com' in api_server_url):
        api_server_url = "api.projectcloudly.com:5001"

    ip = request.META['REMOTE_ADDR']

    try:
        profile = userprofile.objects.get(user=request.user)
    except: pass

    print 'server_url', server_url
    print 'api_server_url', api_server_url

    if(request.GET):

        try:
            xuuid = request.GET['xuuid']
            profile = userprofile.objects.get(agent_hash=xuuid)
        except:
            return HttpResponseForbidden()

        _log_user_activity(profile,"download","/download/agent/","download_agent",ip=ip)

        agent_code = ""
        for line in open('agent.py'):
            if("SECRET = \"\"" in line):
                agent_code += "SECRET = \""+profile.secret+"\"\n"
                continue
            if("API_SERVER = \"\"" in line):
                agent_code += "API_SERVER = \""+api_server_url+"\"\n"
                continue
            agent_code += line

        return HttpResponse(agent_code)

    try:
        agent_download_url = server_url + "download/agent?xuuid="+profile.agent_hash
        print 'agent_download_url', agent_download_url
    except:
        return HttpResponseRedirect("https://raw.githubusercontent.com/ProjectCloudly/Cloudly/master/agent.py")


    return render_to_response('agent_download.html', {'request': request, 'profile':profile,'agent_download_url':agent_download_url,}, context_instance=RequestContext(request))
