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


def admin(request):

	print '--  admin page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	#if not request.user.is_superuser:
	#	print 'anonymous'
	#	return HttpResponseRedirect("/")

	print request.user
	
	users = Profile.objects.all()
	profile = Profile.objects.get(user=request.user)
		
	active_tab = "admin"
	profile.clicks += 1
	profile.save()
	
	users = User.objects.all()
	
	return render_to_response('admin.html', {'users':users,'profile':profile,}, context_instance=RequestContext(request))

