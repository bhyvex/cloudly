# -*- coding: utf-8 -*-

import os
import time
import logging

import base64
try: import cPickle as pickle
except: import pickle

import datetime
import json
#from django.utils import simplejson

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

from amazon import s3_funcs
from amazon import s3_funcs_shortcuts

from cloud_storage.models import Files
from cloud_storage.models import Uploaded_Files

from django.template.defaultfilters import filesizeformat, upper
from django.contrib.humanize.templatetags.humanize import naturalday

from cloudly.templatetags.cloud_extras import clear_filename, get_file_extension

from cloud_vms.models import Cache

import decimal
from django.db.models.base import ModelState


def date_handler(obj):
	return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def ajax_vms_refresh(request):
	
	user = request.user
	
	try:
		profile = userprofile.objects.get(user=request.user)
	except: return HttpResponseRedirect("access denied")
	
	print 'Refreshing', user, 'VMs cache..'
	
	aws_access_key = profile.aws_access_key
	aws_secret_key = profile.aws_secret_key
	aws_ec2_verified = profile.aws_ec2_verified

	aws_virtual_machines = {}

	if aws_ec2_verified:
		
		vms_cache = Cache.objects.get_or_create(user=user)	
		vms_cache = vms_cache[0]
		
		vms_cache.is_updating = True
		vms_cache.save()
		
		aws_regions = profile.aws_enabled_regions.split(',')
		print 'AWS regions', aws_regions
		
		for ec2_region in aws_regions:
			
			if(ec2_region):

				ec2conn = boto.ec2.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
				cloudwatch = boto.ec2.cloudwatch.connect_to_region(ec2_region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

				try:
					reservations = ec2conn.get_all_instances()
				except:
					vms_cache.is_updating = False
					vms_cache.vms_response = ""
					vms_cache.save()
					print vms_cache.is_updating
					print vms_cache.vms_response
					return HttpResponse("access denied")
					
				instances = [i for r in reservations for i in r.instances]

				for instance in instances:
						
					if not instance: continue
	
					instance_metrics = {}
					instance_metrics['instance'] = instance.__dict__					
					aws_virtual_machines[instance.id] = pprint(instance_metrics)
													
					print '** instance', instance.id, instance.private_ip_address

					# XXX workaround to supplement for pickle not working
					#aws_virtual_machines[instance.id]['instance']['groups'] = []
					#aws_virtual_machines[instance.id]['instance']['block_device_mapping'] = []
							
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
					try:
						metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="CPUUtilization")[0]
					except: continue
					
					
					cpu_utilization_datapoints = metric.query(start, end, 'Average', 'Percent')
					#instance_metrics['cpu_utilization_datapoints'] = cpu_utilization_datapoints

					# DiskReadOps
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadOps")[0]
					disk_readops_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_readops_datapoints'] = disk_readops_datapoints

					# DiskWriteOps
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteOps")[0]
					disk_writeops_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_writeops_datapoints'] = disk_writeops_datapoints

					# DiskReadBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadBytes")[0]
					disk_readbytes_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_readbytes_datapoints'] = disk_readbytes_datapoints

					# DiskWriteBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteBytes")[0]
					disk_writebytes_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['disk_writebytes_datapoints'] = disk_writebytes_datapoints
					
					# NetworkIn
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkIn")[0]
					networkin_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['networkin_datapoints'] = networkin_datapoints
					
					# NetworkOut
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkOut")[0]
					networkout_datapoints = metric.query(start, end, 'Average', '')
					#instance_metrics['networkout_datapoints'] = networkout_datapoints

					aws_virtual_machines[instance.id] = instance_metrics


	print 'aws_virtual_machines', aws_virtual_machines

	try:
		vms_cache.vms_response = base64.b64encode(pickle.dumps(aws_virtual_machines, pickle.HIGHEST_PROTOCOL))	
	except:
		vms_cache.vms_response = json.dumps(aws_virtual_machines)
		
	
	
	from django.utils import timezone
	vms_cache.last_seen = timezone.now()
	vms_cache.is_updating = False
	vms_cache.save()
	
	print 'VMs cache was succesfully updated.'
	
	return HttpResponse("ALLDONE")
	
	

def ajax_virtual_machines(request):
	
	print '-- ajax virtual machines'
	
	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	
	
	return render_to_response('ajax_virtual_machines.html', locals(), context_instance=RequestContext(request))

