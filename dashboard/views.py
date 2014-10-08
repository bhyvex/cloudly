# -*- coding: utf-8 -*-

import os
import time
import logging
import datetime
import simplejson
import base64, pickle

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
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity

from amazon import ec2_funcs
from cloud_vms.models import Cache

def home(request):
		
	if not request.user.is_authenticated():
		
		print '--  web:'
		print 'anonymous'
	
		return render_to_response('web.html', locals(), context_instance=RequestContext(request))

	print '--  dashboard:'
	print request.user
	
	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret
	
	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/","home",ip=ip)
	
	#try:
	#print 'vms_cache.vms_response' * 1000
	#vms_cache = Cache.objects.get(user=request.user)
	#vms_respose = base64.b64encode(vms_cache.vms_response)
	#print vms_response
	#except: 
	vms_cached_response = None

	return render_to_response('dashboard.html', {'vms_cached_response':vms_cached_response,}, context_instance=RequestContext(request))


def welcome(request):

	print '--  welcome page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	ip = request.META['REMOTE_ADDR']
	profile = userprofile.objects.get(user=request.user)
	_log_user_activity(profile,"click","/welcome/","welcome",ip=ip)
	

	print request.user
	return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))


def pricing(request):

	print '--  pricing page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	ip = request.META['REMOTE_ADDR']
	profile = userprofile.objects.get(user=request.user)
	_log_user_activity(profile,"click","/pricing/","pricing",ip=ip)


	print request.user
	return render_to_response('pricing.html', locals(), context_instance=RequestContext(request))



def help(request):

	print '--  help page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/help/","help",ip=ip)
	
	http_host = request.META['HTTP_HOST']

	return render_to_response('help.html', {'http_host':http_host, 'profile':profile,'secret':secret,}, context_instance=RequestContext(request))

def security(request):

	print '--  security page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	
	profile = userprofile.objects.get(user=request.user)
	
	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/security/","security",ip=ip)
	
	
	return render_to_response('security.html', {'profile':profile,}, context_instance=RequestContext(request))


