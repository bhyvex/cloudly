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

from cloud_storage.models import Files
from cloud_storage.models import Uploaded_Files

from userprofile.views import _log_user_activity


def user_activity_report(request, user_id):
	
	print '-- admin report user activity', user_id
	
	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	#if not request.user.is_superuser:
	#	print 'anonymous'
	#	return HttpResponseRedirect("/")
	
	print request.user
	
	profile = Profile.objects.get(user=request.user)
	
	user_files = Uploaded_Files.objects.filter(user_id=user_id).order_by('-pk')[:5000]
	
	_log_user_activity(profile,"click","/admin/user/"+str(user_id)+"/report/","user_activity_report")
	
	user_activity = "TODO"
		
	return render_to_response('admin-user-report.html', {'user_files':user_files,'user_activity':user_activity,'profile':profile,}, context_instance=RequestContext(request))
	

	
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
		
			
	users = Profile.objects.all().order_by('-pk')
	files = Uploaded_Files.objects.all().order_by('-pk')[:5000]
	
	_log_user_activity(profile,"click","/admin/","admin")
	
	return render_to_response('admin.html', {'users':users,'files':files,'profile':profile,}, context_instance=RequestContext(request))

