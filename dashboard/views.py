# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

from pprint import pprint

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
from userprofile.views import _log_user_activity

from amazon import ec2_funcs

def home(request):
		
	if not request.user.is_authenticated():
		
		print '--  web:'
		print 'anonymous'
	
		return render_to_response('web.html', locals(), context_instance=RequestContext(request))

	print '-'*100
	print '--  dashboard:'
	print request.user
	
	
	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret
	
	_log_user_activity(profile,"click","/","home")
	
	
	aws_access_key = profile.aws_access_key
	aws_secret_key = profile.aws_secret_key
	aws_ec2_verified = profile.aws_ec2_verified

	aws_virtual_machines = {}
	
	if aws_ec2_verified:
					
		aws_regions = profile.aws_enabled_regions.split(',')
		print 'AWS regions', aws_regions
		
		for ec2_region in aws_regions:
			
			if(ec2_region):

				ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
				cloudwatch = boto.ec2.cloudwatch.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

				reservations = ec2conn.get_all_instances()
				instances = [i for r in reservations for i in r.instances]

				for instance in instances:
					
					instance_metrics = {}
					instance_metrics['instance'] = instance.__dict__
					
					#pprint(instance.__dict__)
										
					print '** name', instance.id
					print '** monitoring', instance.monitoring_state
					
					if(instance.monitoring_state=="disabled"):
						try:
							ec2conn.monitor_instance(str(instance.id))
						except:
							print instance.id, 'instance not in a monitorable state!'.upper()
							print instance.id, 'state:', instance.state
							print instance.id, 'reason:', instance.state_reason['message']
							continue
					
					end = datetime.datetime.utcnow()
					start = end - datetime.timedelta(hours=1)
				
					# ['Minimum', 'Maximum', 'Sum', 'Average', 'SampleCount']
					# ['Seconds', 'Percent', 'Bytes', 'Bits', 'Count', 'Bytes/Second', 'Bits/Second', 'Count/Second']
					
					# CPUUtilization
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="CPUUtilization")[0]
					cpu_utilization_datapoints = metric.query(start, end, 'Average', 'Percent')
					instance_metrics['cpu_utilization_datapoints'] = cpu_utilization_datapoints

					# DiskReadOps
					#metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadOps")[0]
					#disk_readops_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_readops_datapoints'] = disk_readops_datapoints

					# DiskWriteOps
					#metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteOps")[0]
					#disk_writeops_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_writeops_datapoints'] = disk_writeops_datapoints

					# DiskReadBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadBytes")[0]
					disk_readbytes_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_readbytes_datapoints'] = disk_readbytes_datapoints

					# DiskWriteBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteBytes")[0]
					disk_writebytes_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_writebytes_datapoints'] = disk_writebytes_datapoints
					
					# NetworkIn
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkIn")[0]
					networkin_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['networkin_datapoints'] = networkin_datapoints
					
					# NetworkOut
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkOut")[0]
					networkout_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['networkout_datapoints'] = networkout_datapoints

					aws_virtual_machines[instance.id] = instance_metrics

	private_virtual_machines = {}
	
	return render_to_response('dashboard.html', {'private_virtual_machines':private_virtual_machines, 'aws_virtual_machines':aws_virtual_machines,}, context_instance=RequestContext(request))


def welcome(request):

	print '--  welcome page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	profile = userprofile.objects.get(user=request.user)
	_log_user_activity(profile,"click","/welcome/","welcome")
	

	print request.user
	return render_to_response('welcome.html', locals(), context_instance=RequestContext(request))


def pricing(request):

	print '--  pricing page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	profile = userprofile.objects.get(user=request.user)
	_log_user_activity(profile,"click","/pricing/","pricing")


	print request.user
	return render_to_response('pricing.html', locals(), context_instance=RequestContext(request))



def help(request):

	print '--  help page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user

	user = request.user
	profile = userprofile.objects.get(user=request.user)
	secret = profile.secret

	_log_user_activity(profile,"click","/help/","help")
	
	http_host = request.META['HTTP_HOST']

	return render_to_response('help.html', {'http_host':http_host, 'profile':profile,'secret':secret,}, context_instance=RequestContext(request))

def security(request):

	print '--  security page:'

	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	
	profile = userprofile.objects.get(user=request.user)
	
	_log_user_activity(profile,"click","/security/","security")
	
	
	return render_to_response('security.html', {'profile':profile,}, context_instance=RequestContext(request))


