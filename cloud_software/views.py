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

from cloud_software.models import Packages
from cloud_software.models import Tags
from cloud_software.models import Tag

def cloud_software_add_new(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	if not request.user.is_superuser:
		return HttpResponse("access denied")

	print '-- cloud software add new:'
	print request.user

	if request.POST:

		print request.POST

		icon = request.POST['icon']
		title = request.POST['title']
		description = request.POST['description']
		package_name = request.POST['package_name']
		package_link = request.POST['package_link']
		package_ami = request.POST['package_ami']

		package = Packages.objects.create(
			icon = icon,
			title = title,
			description = description,
			package_name = package_name,
			package_link = package_link,
			package_ami = package_ami,
			)

		print 'package', package
		print 'Adding tags..'

		comma_separated_tags = request.POST['comma_separated_tags']

		print 'comma_separated_tags', comma_separated_tags

		for tag_ in comma_separated_tags.split(','):

			tag_ = Tag.objects.get_or_create(name=tag_)
			tag_asociated = Tags.objects.get_or_create(tag=tag_[0],package=package)

			print '\ttag', tag_
			print '\ttag_asociated', tag_asociated

		return HttpResponseRedirect("/cloud/software/")


	return render_to_response('cloud_software_add_new.html', {}, context_instance=RequestContext(request))

def cloud_software(request):

	print '-- cloud_software:'

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	packages = Packages.objects.all().order_by('-pk')
	tags = Tag.objects.all()

	print request.user

	return render_to_response('cloud_software.html', {'user':user,'profile':profile,'packages':packages,'tags':tags,}, context_instance=RequestContext(request))
