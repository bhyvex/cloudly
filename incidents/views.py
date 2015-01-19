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

@login_required()
def incidents(request):	

	print '-- system logs:'

	user = request.user
	profile = Profile.objects.get(user=request.user)
	secret = profile.secret

	print request.user
	
	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/logs/","logs",ip=ip)

	user = request.user
	user.last_login = datetime.datetime.now()
	user.save()
	
	return render_to_response('incidents.html', {'profile':profile,}, context_instance=RequestContext(request))
