# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime
import socket

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly

@login_required()
def server_detail(request, uuid):
	
	user = request.user
	user.last_login = datetime.datetime.now()
	user.save()

	print '-- server detail:'
	print request.user, 'server', uuid
	
	uuid = uuid.replace('-',':')
	server = mongo.servers.find_one({'uuid':uuid,})

	print 'uuid', uuid
	print 'server', server
	
	if not server:
		return HttpResponse("access denied")
		
	loadavg = mongo.loadavg.find({'uuid':uuid,}).sort('_id',-1).limit(10)
	mem_usage = mongo.memory_usage.find({'uuid':uuid,}).sort('_id',-1).limit(10)
	disks_usage = mongo.disks_usage.find({'uuid':uuid,}).sort('_id',-1).limit(10)
	cpu_usage = mongo.cpu_usage.find({'uuid':uuid,}).sort('_id',-1).limit(10)
	activity = mongo.activity.find({'uuid':uuid,}).sort('_id',-1).limit(5)

	# XXX
	#ip = request.META['REMOTE_ADDR']
	#profile = userprofile.objects.get(user=request.user)
	#_log_user_activity(profile,"click","/server/","admin",ip=ip)

	return render_to_response('private_server_detail.html', {"uuid":uuid,"server":server,"loadavg":loadavg,"mem_usage":mem_usage, "cpu_usage":cpu_usage, "disks_usage":disks_usage, "activity":activity,}, context_instance=RequestContext(request))

@login_required()
def servers(request):

	user = request.user
	user.last_login = datetime.datetime.now()
	user.save()

	print '-- servers:'
	print request.user

	profile = userprofile.objects.get(user=request.user)

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/servers/","servers",ip=ip)

	#if request.user.is_superuser:
	#	servers  = mongo.servers.find().sort('_id',-1)
	#else:
	servers = mongo.servers.find({'secret':profile.secret,}).sort('_id',-1)
	
	servers_count = servers.count()
	
	print 'servers', servers
	print 'servers_count', servers_count

	#server_addr = socket.gethostbyname(socket.gethostname())
	server_addr = request.get_host()
	
	return render_to_response('private_servers.html', {'server_addr':server_addr, 'servers':servers,'servers_count':servers_count,}, context_instance=RequestContext(request))
