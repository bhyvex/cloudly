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
from userprofile.models import Profile as userprofile


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
	
	aws_access_key = profile.aws_access_key
	aws_secret_key = profile.aws_secret_key
	aws_is_verified = profile.aws_is_verified
	
	print 'aws_is_verified', aws_is_verified
	
	if aws_is_verified:
		ec2_regions = boto.ec2.regions()
		for ec2_region in ec2_regions:
			print 'region:', ec2_region.name
	
	
	return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))


def welcome(request):

	print '--  welcome page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))
	
def help(request):

	print '--  help page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	return render_to_response('help.html', locals(), context_instance=RequestContext(request))

def security(request):

	print '--  security page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	return render_to_response('security.html', locals(), context_instance=RequestContext(request))


