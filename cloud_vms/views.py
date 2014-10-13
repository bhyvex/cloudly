# -*- coding: utf-8 -*-

import os
import time
import logging

import base64
try: import cPickle as pickle
except: import pickle

import datetime
from django.utils import timezone

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
#from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType

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
	except: return HttpResponseRedirect("/")
	
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
					instance_metrics['groups'] = {}
					instance_metrics['block_device_mapping'] = {}
						
					print '** instance', instance.id, instance.private_ip_address
					
					volumes = []
					for volume in ec2conn.get_all_volumes(filters={'attachment.instance-id': instance.id}):
						volumes.append([volume.id, volume.iops, volume.size,])

					groups = []
					for group in instance.__dict__['groups']:
						groups.append([group.id, group.name,])

					instance_metrics['groups'] = groups
					instance_metrics['block_device_mapping'] = volumes
					instance_metrics['architecture'] = instance.architecture
					instance_metrics['client_token'] = instance.client_token
					instance_metrics['dns_name'] = instance.dns_name
					instance_metrics['private_ip_address'] = instance.private_ip_address
					instance_metrics['hypervisor'] = instance.hypervisor
					instance_metrics['id'] = instance.id
					instance_metrics['image_id'] = instance.image_id
					instance_metrics['instance_type'] = instance.instance_type
					instance_metrics['ip_address'] = instance.ip_address
					instance_metrics['key_name'] = instance.key_name
					instance_metrics['launch_time'] = instance.launch_time
					instance_metrics['monitored'] = instance.monitored
					instance_metrics['persistent'] = instance.persistent
					instance_metrics['ramdisk'] = instance.ramdisk
					instance_metrics['root_device_name'] = instance.root_device_name
					instance_metrics['root_device_type'] = instance.root_device_type
					instance_metrics['tags'] = instance.tags
					instance_metrics['virtualization_type'] = instance.virtualization_type
					instance_metrics['vpc_id'] = instance.vpc_id
					instance_metrics['region'] = {"endpoint":instance.region.endpoint,"name":instance.region.name,}				
					instance_metrics['state'] = {"state":instance.state,"code":instance.state_code,"state_reason":instance.state_reason,}

				
					try:
						ec2conn.monitor_instance(str(instance.id))
					except:
						print instance.id, 'instance not in a monitorable state!'.upper()
						continue
					
					
					# Here is where you define start - end for the Logs...............
					end = datetime.datetime.utcnow()
					start = end - datetime.timedelta(hours=1)
				
					# And the list of possible values on the aws response....
					# ['Minimum', 'Maximum', 'Sum', 'Average', 'SampleCount']
					# ['Seconds', 'Percent', 'Bytes', 'Bits', 'Count', 'Bytes/Second', 'Bits/Second', 'Count/Second']
					# print ec2conn.list_metrics()
					
					# CPUUtilization
					try:
						metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="CPUUtilization")[0]
					except: continue
					
					print '-_'*1000
					cpu_utilization_datapoints_ = []
					datapoints = metric.query(start, end, 'Average', 'Percent')
					for i in datapoints: 
						cpu_utilization_datapoints_.append(i)
					pprint(cpu_utilization_datapoints_)
					print type(cpu_utilization_datapoints_)
					
					instance_metrics['cpu_utilization_datapoints'] = json.dumps(cpu_utilization_datapoints_)

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


		print 'aws_virtual_machines'

		# XXX Note This is how this should be - but I get this fucked up error on the prod......
		# XXX Note Can't pickle <type '_hashlib.HASH'>: attribute lookup _hashlib.HASH failed
		# XXX Note Specifically, it's the Python Bug that "cannot be fixed" http://bugs.python.org/issue11771
		# XXX Note Quote: There is no way to implement generic pickling for hash objects that would work across all implementations.
		#try:
		vms_cache.vms_response = base64.b64encode(pickle.dumps(aws_virtual_machines, pickle.HIGHEST_PROTOCOL))	
		#except:
		#	return HttpResponse("Fuck shit wank bugger Can't pickle <type '_hashlib.HASH'>: attribute lookup _hashlib.HASH failed problem..")
		
		print 'xxxxx', aws_virtual_machines

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

