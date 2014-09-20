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
	return HttpResponse("working on this currently " + str(file_id))

def cloud_dropzone(request):
	
	print '-- cloud_storage:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

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
		return ""

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')


	# XXX populate this from html instead..
	counter = 0
	fobj = []
	for f in uploaded_files:
		row = []
		counter+=1
		row.append('<a href="/media/'+str(f.file.file)+'">'+str(counter)+'</a>')
		row.append(naturalday(f.date_created))
		row.append('<a href="/media/'+str(f.file.file)+'" target="_blank">'+clear_filename(f.file.file)+'</a> <small><a href="#" id="name" data-type="text" data-pk="1" data-original-title="Name this file" class="editable editable-click">create alias</a></small>')
		row.append(filesizeformat(f.file.file.size))
		row.append(upper(get_file_extension(f.file.file)))
		row.append('<span class="label label-warning">Synchronising..</span>')
		if (not f.is_shared):
			row.append(' <a class="btn btn-success" href="#"><i class="fa fa-search-plus "></i></a> <a class="btn btn-info" href="/media/'+str(f.file.file)+'" target="_blank"><i class="fa fa-cloud-download "></i></a> <a class="btn btn-info" href="#" target="_blank"><i class="fa fa-share "></i></a> <a class="btn btn-danger" href="/cloud/file/'+str(f.id)+'/delete"><i class="fa fa-trash-o "></i></a>')
		else:
			row.append(' <a class="btn btn-warning" href="/password/protect/file"><i class="fa fa-key "></i></a> <a class="btn btn-danger" href="#"><i class="fa fa-trash-o "></i></a><button type="button" class="btn btn-link"><i class="fa fa-link"></i> Share Link</button><span class="label label-default">'+str(f.share_link_clicks_count)+'</span>')
		fobj.append(row)

	json = { 'data': fobj }

#	return render_to_response('cloud_storage-list.html', {'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))
	return HttpResponse(simplejson.dumps(json), mimetype='application/json')

