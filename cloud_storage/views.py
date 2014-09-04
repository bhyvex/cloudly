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
from userprofile.models import Profile as userprofile

from amazon import s3_funcs
from amazon import s3_funcs_shortcuts

from django import forms
from forms import UploadFileForm
from cloud_storage.models import Files
from cloud_storage.models import Uploaded_Files


def cloud_dropzone(request):
	
	print '-- cloud_storage:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = Files(file=request.FILES['file'])
			new_file.save()
			Uploaded_Files.objects.create(file=new_file,user=request.user)
  
	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')
	
	return render_to_response('cloud_dropzone.html', {'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))
	
	

def cloud_storage(request):

	print '-- cloud_storage:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = Files(file=request.FILES['file'])
			new_file.save()
			Uploaded_Files.objects.create(file=new_file,user=request.user)
  
	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')

	# XXX batch sync files to the S3.....
	
	return render_to_response('cloud_storage.html', {'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))

def ajax_cloud_storage(request):

	print '-- ajax_cloud_storage:'

	if not request.user.is_authenticated():
		return ""

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')

	return render_to_response('cloud_storage-list.html', {'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))


