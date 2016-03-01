# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch

from django.contrib.auth.models import User
from userprofile.models import Profile
from userprofile.views import _log_user_activity


def aws_test(request):

    aws = AWS.objects.get(user=request.user)
    AWS_ACCESS_KEY=aws.AWS_ACCESS_KEY
    AWS_ACCESS_SECRET=aws.AWS_SECRET_KEY

    aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)

    reservations = aws_conn.get_all_reservations()

    cloudwatch = boto.connect_cloudwatch()
    metrics = cloudwatch.list_metrics()

    print 'AWS IMs metrics', metrics

    user = request.user
    user.last_login = datetime.datetime.now()
    user.save()


    for reservation in reservations:

        instances = reservation.instances
        for instance in instances:

            print 'id', instance.id
            print 'attributes', instance.__dict__

    return HttpResponse(True)
