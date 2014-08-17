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

import boto.ec2
import boto.ec2.cloudwatch

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile

def test(request):
	return HttpResponse(True)

