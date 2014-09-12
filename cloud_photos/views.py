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

# As per Browsers Image format support: http://en.wikipedia.org/wiki/Comparison_of_web_browsers#Image_format_support
# 

def cloud_photos(request):

	print '-- cloud_photos:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user
	
	cloud_storage_menu_open = True

	return render_to_response('cloud_pictures.html', {'profile':profile,'cloud_storage_menu_open':cloud_storage_menu_open,}, context_instance=RequestContext(request))

