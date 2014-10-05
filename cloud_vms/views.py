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

from cloud_storage.models import Files
from cloud_storage.models import Uploaded_Files

from django.template.defaultfilters import filesizeformat, upper
from django.contrib.humanize.templatetags.humanize import naturalday
from cloudly.templatetags.cloud_extras import clear_filename, get_file_extension


def ajax_vms_refresh(request):
	# XXX work on this
	import time
	import random
	time.sleep(random.randint(1,5))
	return HttpResponse("ALLDONE")


def ajax_virtual_machines(request):
	
	print '-- ajax virtual machines'
	
	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	
	
	return render_to_response('ajax_virtual_machines.html', locals(), context_instance=RequestContext(request))

