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


def logs(request):	

	print '-- system logs:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = Profile.objects.get(user=request.user)
	secret = profile.secret

	print request.user
	
	_log_user_activity(profile,"click","/logs/","logs")

	
	return render_to_response('logs.html', {'profile':profile,}, context_instance=RequestContext(request))
