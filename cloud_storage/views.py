# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime
import json

from pprint import pprint

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import simplejson

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

from django.template.defaultfilters import filesizeformat, upper
from django.contrib.humanize.templatetags.humanize import naturalday
from cloudly.templatetags.cloud_extras import clear_filename, get_file_extension


def delete_file(request, file_id):

	print '-- delete_file:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print 'user', request.user

	try:
		f = Uploaded_Files.objects.get(pk=file_id)
		if(f.user!=request.user):
			return HttpResponse("access denied")
	except: 
		return HttpResponse("access denied")
	
	if(request.GET):
		if(request.GET['confirm']=="True"):
			f.delete()
			return HttpResponseRedirect("/cloud/storage/")
	
	return render_to_response('cloud_file_delete.html', {'f':f,'profile':profile,}, context_instance=RequestContext(request))


def cloud_dropzone(request):
	
	print '-- cloud_storage:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print 'user', request.user

	uploaded_files = []

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			new_file = Files(file=request.FILES['file'])
			new_file.save()
			uploaded_file = Uploaded_Files.objects.create(file=new_file,user=request.user)
  
	cloud_storage_menu_open = True
	
	return render_to_response('cloud_dropzone.html', {'cloud_storage_menu_open':cloud_storage_menu_open,'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))
	
def cloud_sharing(request):
	
	print '-- cloud sharing:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print 'user', request.user
	
	return render_to_response('cloud_sharing.html', {'profile':profile,}, context_instance=RequestContext(request))

def dropzone_uploader(request):

	print '-- dropzone_uploader:'


	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	print request.user

	if request.method == 'POST':

		#form = UploadFileForm(request.POST, request.FILES)
		#if form.is_valid():
		#print 'valid form', form

		new_file = Files(file=request.FILES['files[]'])
		new_file.save()
		f = Uploaded_Files.objects.create(file=new_file,user=request.user)

		file_thumbnailUrl = "/media/"+str(new_file.file)
		file_name = new_file.file
		file_size = os.path.getsize("media/"+str(new_file.file))
<<<<<<< HEAD
		file_type = str(new_file.file).split('.')[1:][0]
=======
		file_type = str(new_file.file).split('.')[-1:][0]
>>>>>>> FETCH_HEAD

		response_type = "application/json"
		if "text/html" in request.META["HTTP_ACCEPT"]: response_type = "text/html"
                jsonData = {}
                    
                jsonData['thumbnailUrl'] = str(file_thumbnailUrl)
                jsonData['name'] = str(file_name)
                jsonData['size'] = str(file_size)
                jsonData['type'] = str(file_type)
                
                jsonData = {"files" : [jsonData]}
		#simple_json = """{"thumbnailUrl": "%s", "name": "%s", "size": "%s", "type": "%s"}""" %(file_thumbnailUrl,file_name,file_size,file_type,)
		simple_json = json.dumps(jsonData, separators=(',',':'))
		return HttpResponse(simple_json, mimetype=response_type)


	return HttpResponse("invalid form")


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
	cloud_storage_menu_open = True

	# XXX batch sync files to the S3.....
	
	return render_to_response('cloud_storage.html', {'cloud_storage_menu_open':cloud_storage_menu_open,'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))

def ajax_cloud_storage(request):

	print '-- ajax_cloud_storage:'

	if not request.user.is_authenticated():
		return HttpResponse("access denied")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')

	return render_to_response('cloud_storage-list.html', {'uploaded_files':uploaded_files,'profile':profile,}, context_instance=RequestContext(request))

