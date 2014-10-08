# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

from pprint import pprint

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

from amazon import ec2_funcs

	
def devel(request, dev=""):

	print '--  devel page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user

	ip = request.META['REMOTE_ADDR']
	profile = Profile.objects.get(user=request.user)
	_log_user_activity(profile,"click","/devel/","devel",ip=ip)	
	
	active_tab = "devel"
	
	user = request.user
	user.last_login = datetime.datetime.now()
	user.save()
	
	
	return render_to_response('devel'+dev+'.html', {'active_tab':active_tab,}, context_instance=RequestContext(request))

