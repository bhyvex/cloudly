# -*- coding: utf-8 -*-

import os
import time
import logging
import unicodedata

import string, pickle
from random import choice

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from userprofile.models import Activity
from userprofile.models import Profile as userprofile

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

logger = logging.getLogger(__name__)

from django.core.mail import send_mail


def _remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()


def _log_user_activity(userprofile, activity, link):
	
	activity = Activity.objects.create(user=userprofile.user,activity=activity,link=link)
	
	return activity


def user_logout(request):
	
	print '-- logout'
	
	try:
		logout(request)
	except:
		pass
		
	print request.user
	
	return HttpResponseRedirect("/goodbye/")



def goodbye(request):

	return render_to_response('goodbye.html', {}, context_instance=RequestContext(request))


def register(request):

	print '-- registration:'

	err = None

	if request.POST:

		name = request.POST[u'username']
		email = request.POST[u'email']
		username = email
		
		try:
			if(request.POST['agree']!='on'):
				err = "must_agree_tos"
		except: err = "must_agree_tos"

		password1 = request.POST[u'password1']
		#password2 = request.POST[u'password2']
		password2 = password1

		print username


		if not password1 or not password2:
			err = "empty_password"
			print err

		if(password1 != password2):
			err = "password_mismatch"
			print err

		if not err:

			passwd = password1

			try:
				User.objects.create_user(username, email, passwd)
			except:
				err = "duplicate_username"
				print err

			if not err:

				user = authenticate(username=username, password=passwd)

				if(user):

					secret = (''.join([choice(string.digits) for i in range(3)]) + '-' + \
						''.join([choice(string.letters + string.digits) for i in range(4)]) + '-' + \
						''.join([choice(string.digits) for i in range(5)])).upper()

					username = _remove_accents(username)
					#name = _remove_accents(name)

					userprofile.objects.get_or_create(user=user,secret=secret,name=name,language="EN")
					login(request, user)

					request.session['language'] = "us"
					
					print 'new user registered'
					print username

					return HttpResponseRedirect("/welcome/")


	return render_to_response('register.html', {'err':err,}, context_instance=RequestContext(request))


def auth(request):
	
	print '-- auth:'
	
	if(request.method == 'POST'):

		post = request.POST
		
		print post
		
		try:
			email = request.POST['username']
			passwprd = request.POST['password']
		except:
			print 'failed login code:1'
			return HttpResponseRedirect("/register")

		
		try:
			user = User.objects.get(email=email)
		except:
			print 'failed login code:2'
			return HttpResponseRedirect("/register")

		try:
			user = authenticate(username=user.username, password=passwprd)
			login(request, user)
		except:
			print 'failed login code:3'
			return HttpResponseRedirect("/register")
			
		print 'user logged in', user
		
		return HttpResponseRedirect("/")
		
	
	return render_to_response('login.html', {}, context_instance=RequestContext(request))


def cloud_settings(request):
	
	print '-- cloud settings:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user
	
	aws_regions = {
		"ap-northeast-1":"Asia Pacific (Tokyo) Region",
		"ap-southeast-1":"Asia Pacific (Singapore) Region",
		"ap-southeast-2":"Asia Pacific (Sydney) Region",
		"eu-west-1":"EU (Ireland) Region",
		"sa-east-1":"South America (Sao Paulo) Region",
		"us-east-1":"US East (Northern Virginia) Region",
		"us-west-1":"US West (Northern California) Region",
		"us-west-2":"US West (Oregon) Region",
	}

	return render_to_response('cloud_settings.html', {'aws_regions':aws_regions,'profile':profile,'secret':secret,}, context_instance=RequestContext(request))
	

def lock(request):
	
	print '-- lock screen:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	return render_to_response('lock.html', {'profile':profile,}, context_instance=RequestContext(request))

	
def change_password(request):

	print '-- change password:'


	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	error = None

	if(request.POST):

		current_passwd = request.POST['current_passwd']
		new_passwd = request.POST['new_passwd']
		new_passwd_repeat = request.POST['new_passwd_repeat']

		if(new_passwd != new_passwd_repeat):
			error = "Passwords do not match."

		user = authenticate(username=request.user, password=current_passwd)
		if(not user): 
			error = "Wrong password."

		if(not error):
			user.set_password(new_passwd)
			user.save()
			return HttpResponseRedirect("/account/settings/")

	return render_to_response('account_change_password.html', {'error':error,}, context_instance=RequestContext(request))

def account_settings(request):

	print '-- account settings:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	print request.user

	# this is how to get the list of all available aws regions..
	#ec2_regions = boto.ec2.regions()
	#for ec2_region in ec2_regions:
	#	print '- ec2 region:', ec2_region.name

	return render_to_response('account.html', {'user':user,'profile':profile,}, context_instance=RequestContext(request))

