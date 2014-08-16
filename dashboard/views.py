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

def home(request):
		
	if not request.user.is_authenticated():
		
		print '--  web:'
		print 'anonymous'
	
		return render_to_response('web.html', locals(), context_instance=RequestContext(request))

	print '--  dashboard:'
	print 'anonymous'
	
	return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))


def welcome(request):

	print '--  welcome page:'

	if not request.user.is_authenticated():

		print 'anonymous'

		return HttpResponseRedirect("/")


	print request.user

	return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))