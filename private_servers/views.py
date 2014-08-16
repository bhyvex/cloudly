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

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile

logger = logging.getLogger(__name__)

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly

def servers(request):
		
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	print '-- servers:'
	print request.user

	profile = userprofile.objects.get(user=request.user)

	if request.user.is_superuser:
		servers  = mongo.servers.find().sort('_id',-1)
	else:
		servers = mongo.servers.find({'secret':profile.secret,}).sort('_id',-1)
	
	servers_count = servers.count()
	
	print 'servers', servers
	print 'servers_count', servers_count

	return render_to_response('private_servers.html', {'profile':profile, 'servers':servers,'servers_count':servers_count,}, context_instance=RequestContext(request))
