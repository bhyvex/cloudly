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
from userprofile.models import Profile
from userprofile.views import _log_user_activity


def devel(request):
    return render_to_response('devel.html', {'request':request,}, context_instance=RequestContext(request))
