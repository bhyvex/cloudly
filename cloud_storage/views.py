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

from userprofile.views import _log_user_activity

from PIL import Image


supported_image_file_types = [ 'bmp','dib','dcx','eps','ps','gif','im','jpg','jpe','jpeg', \
			'pcd','pcx','png','pbm','pgm','ppm','psd','tif','tiff','xbm','xpm',]


def _resize_image(img, box, fit, out):
	# Pre-resize image with factor 2, 4, 8 and fast algorithm
	factor = 1
	while img.size[0]/factor > 2*box[0] and img.size[1]*2/factor > 2*box[1]:
		factor *=2
	if factor > 1:
		img.thumbnail((img.size[0]/factor, img.size[1]/factor), Image.NEAREST)

	# Calculate the cropping box and get the cropped part
	if fit:
		x1 = y1 = 0
		x2, y2 = img.size
		wRatio = 1.0 * x2/box[0]
		hRatio = 1.0 * y2/box[1]
		if hRatio > wRatio:
			y1 = int(y2/2-box[1]*wRatio/2)
			y2 = int(y2/2+box[1]*wRatio/2)
		else:
			x1 = int(x2/2-box[0]*hRatio/2)
			x2 = int(x2/2+box[0]*hRatio/2)
		img = img.crop((x1,y1,x2,y2))

	# Resize the image with best quality algorithm ANTI-ALIAS
	img.thumbnail(box, Image.ANTIALIAS)
	# Save it into a file-like object
	img.save(out, "JPEG", quality=75)


def _work_thumbnail(file_object):
	
	f = file_object
	
	filename = "media/" + str(f.file.file)
	file_type = str(f.file.file).split('.')[-1:][0].lower()

	if(file_type in supported_image_file_types):
		
		image = Image.open(filename)
		thumbnail_dimensions = [100,100]
		thumb_filename = filename.split('.')[:-1][0] + '-thumb' + str(thumbnail_dimensions[0]) + 'x' + str(thumbnail_dimensions[1]) + '.' + file_type
		
		thumb = open(thumb_filename,'wb+')
		try:
			_resize(image, thumbnail_dimensions, True, thumb)
		except:
			print '** failed to convert', 

		thumb.close()
		f.thumbnail_pic1 = thumb_filename
		f.save()

	return f.thumbnail_pic1



def delete_file(request, file_id):

	print '-- delete_file:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	_log_user_activity(profile,"click","/delete/file/"+str(file_id)+"/delete/","delete_file")

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
	
	print '-- cloud dropzone:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	_log_user_activity(profile,"click","/cloud/dropzone/","cloud_dropzone")

	print 'user', request.user

	uploaded_files = []

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			
			new_file = Files(file=request.FILES['file'])
			new_file.save()
			
			uploaded_file = Uploaded_Files.objects.create(file=new_file,user=request.user)

			file_size = os.path.getsize("media/"+str(new_file.file))
			file_type = str(new_file.file).split('.')[-1:][0]

			uploaded_file.size = file_size
			uploaded_file.file_type = file_type
			uploaded_file.save()
			  
	cloud_storage_menu_open = True
	
	return render_to_response('cloud_dropzone.html', {'cloud_storage_menu_open':cloud_storage_menu_open,'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))
	
def cloud_sharing(request):
	
	print '-- cloud sharing:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	_log_user_activity(profile,"click","/cloud/sharing/","cloud_sharing")

	print 'user', request.user
	
	return render_to_response('cloud_sharing.html', {'profile':profile,}, context_instance=RequestContext(request))


#######################################################################################################################

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
		file_type = str(new_file.file).split('.')[-1:][0]

		f.size = file_size
		f.file_type = file_type
		f.save()
		
		_work_thumbnail(f)
		

		response_type = "application/json"
		if "text/html" in request.META["HTTP_ACCEPT"]: 
			response_type = "text/html"

		jsonData = {}
		jsonData['thumbnailUrl'] = str(file_thumbnailUrl)
		jsonData['name'] = str(file_name)
		jsonData['size'] = str(file_size)
		jsonData['type'] = str(file_type)
		jsonData = {"files" : [jsonData]}

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
	
	_log_user_activity(profile,"click","/cloud/storage/","cloud_storage")
		

	if request.method == 'POST':
		
		form = UploadFileForm(request.POST, request.FILES)
		
		if form.is_valid():
		
			new_file = Files(file=request.FILES['file'])
			new_file.save()

			f = Uploaded_Files.objects.create(file=new_file,user=request.user)
			file_name = new_file.file
			file_size = os.path.getsize("media/"+str(new_file.file))
			file_type = str(new_file.file).split('.')[-1:][0]
			f.size = file_size
			f.file_type = file_type
			f.save()
			
			_work_thumbnail(f)
			


	uploaded_files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')
	cloud_storage_menu_open = True

	# XXX batch sync files to the S3.....
	
	return render_to_response('cloud_storage.html', {'cloud_storage_menu_open':cloud_storage_menu_open,'uploaded_files':uploaded_files,'user':user,'profile':profile,}, context_instance=RequestContext(request))

#######################################################################################################################


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

