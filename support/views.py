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

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity


def support(request):

	print '-- support:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/support/","support",ip=ip)

	return render_to_response('support.html', {'user':user,'profile':profile,}, context_instance=RequestContext(request))


def support_add_new(request):
	print '-- add a new support ticket:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/support/add/new/","support_add_new",ip=ip)

	return render_to_response('support-add-new.html', {'user':user,'profile':profile,}, context_instance=RequestContext(request))


def support_devel_ticket(request):

	print '-- support_devel_ticket:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/support/devel/ticket","support_devel_ticket",ip=ip)

	return render_to_response('support-ticket.html', {'user':user,'profile':profile,}, context_instance=RequestContext(request))
