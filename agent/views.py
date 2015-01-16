# -*- coding: utf-8 -*-

import os
import time
import logging
import datetime
import base64, pickle

from pprint import pprint

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

from django.contrib.auth.decorators import login_required


@login_required()
def download(request):
	return HttpResponse("working on this currently")
