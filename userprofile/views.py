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
from userprofile.models import Profile as userprofile

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

logger = logging.getLogger(__name__)

from django.core.mail import send_mail


def _remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

def user_logout(request):
	
	print '-- logout'
	
	try:
		logout(request)
	except:
		pass
		
	print request.user
	
	return HttpResponseRedirect("/")


def register(request):

	print '-- registration:'

	err = None

	if request.POST:

		username = request.POST[u'username']
		email = request.POST[u'email']
		username = email

		password1 = request.POST[u'password1']
		password2 = request.POST[u'password2']

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

					userprofile.objects.get_or_create(user=user,secret=secret,name=username,language="EN")
					login(request, user)

					request.session['language'] = "us"
					
					send_mail('New user has registered.', 'New user ' + request.user.email + ' has registered.', 'admin@cloud306.com', ['jparicka@gmail.com'], fail_silently=True)

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

