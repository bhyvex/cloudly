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

from cloud_storage.models import Files
from cloud_storage.models import Uploaded_Files

BROWSERS_FORMATS = ["JPG", "JPEG", "GIF", "PNG", "APNG", "MNG", "TIFF", "SVG", "PDF", "XBM", "BMP",]
# As per Browsers Image format support: http://en.wikipedia.org/wiki/Comparison_of_web_browsers#Image_format_support

def cloud_photos(request):

	print '-- cloud_photos:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user
	
	print '- searching for pictures'
	
	files = Uploaded_Files.objects.filter(user=request.user).order_by('-pk')
	files_pictures = []
	for f in files:
		
		f_extension = str(f.file.file).split('.')[-1:][0].upper()
				
		if f_extension in BROWSERS_FORMATS:
			print '- mrdka', f_extension, f.file.file
			files_pictures.append(f)
		else:
			print '* skipping', f_extension, f.file.file

	
	
	cloud_storage_menu_open = True

	return render_to_response('cloud_pictures.html', {'BROWSERS_FORMATS':BROWSERS_FORMATS, 'files_pictures':files_pictures, 'profile':profile,'cloud_storage_menu_open':cloud_storage_menu_open,}, context_instance=RequestContext(request))

