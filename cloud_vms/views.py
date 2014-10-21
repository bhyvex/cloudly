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

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile
from userprofile.views import _log_user_activity

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
					instance_metrics['instance'] = {}
											
					print '** instance', instance.id, instance.private_ip_address
					
					volumes = []
					for volume in ec2conn.get_all_volumes(filters={'attachment.instance-id': instance.id}):
						volumes.append([volume.id, volume.iops, volume.size,])

					groups = []
					for group in instance.__dict__['groups']:
						groups.append([group.id, group.name,])

					instance_metrics['id'] = instance.id
					instance_metrics['user_id'] = request.user.id
					instance_metrics['instance']['user_id'] = request.user.id
					instance_metrics['instance']['groups'] = groups
					instance_metrics['instance']['block_device_mapping'] = volumes
					instance_metrics['instance']['architecture'] = instance.architecture
					instance_metrics['instance']['client_token'] = instance.client_token
					instance_metrics['instance']['dns_name'] = instance.dns_name
					instance_metrics['instance']['private_ip_address'] = instance.private_ip_address
					instance_metrics['instance']['hypervisor'] = instance.hypervisor
					instance_metrics['instance']['id'] = instance.id
					instance_metrics['instance']['image_id'] = instance.image_id
					instance_metrics['instance']['instance_type'] = instance.instance_type
					instance_metrics['instance']['ip_address'] = instance.ip_address
					instance_metrics['instance']['key_name'] = instance.key_name
					instance_metrics['instance']['launch_time'] = instance.launch_time
					instance_metrics['instance']['monitored'] = instance.monitored
					instance_metrics['instance']['persistent'] = instance.persistent
					instance_metrics['instance']['ramdisk'] = instance.ramdisk
					instance_metrics['instance']['root_device_name'] = instance.root_device_name
					instance_metrics['instance']['root_device_type'] = instance.root_device_type
					instance_metrics['instance']['tags'] = instance.tags
					instance_metrics['instance']['virtualization_type'] = instance.virtualization_type
					instance_metrics['instance']['vpc_id'] = instance.vpc_id
					instance_metrics['instance']['region'] = {"endpoint":instance.region.endpoint,"name":instance.region.name,}				
					instance_metrics['instance']['state'] = {"state":instance.state,"code":instance.state_code,"state_reason":instance.state_reason,}
					
					aws_virtual_machines[instance.id] = instance_metrics
					
					print 'Updating cache. '*100
					print instance.platform, instance.product_codes

					try:
						ec2conn.monitor_instance(str(instance.id))
					except:
						print instance.id, 'instance not in a monitorable state!!'.upper()
						#pprint(instance_metrics)
						continue
					

					# Here is where you define start - end for the Logs...............
					end = datetime.datetime.utcnow()
					start = end - datetime.timedelta(hours=1)
				
					# This is how you list all possible values on the response....
					# print ec2conn.list_metrics()
					
					# CPUUtilization
					try:
						metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="CPUUtilization")[0]
					except: continue
					
					cpu_utilization_datapoints = metric.query(start, end, 'Average', 'Percent')
					instance_metrics['cpu_utilization_datapoints'] = json.dumps(cpu_utilization_datapoints,default=date_handler)

					# DiskReadOps
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadOps")[0]
					disk_readops_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_readops_datapoints'] = json.dumps(disk_readops_datapoints,default=date_handler)

					# DiskWriteOps
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteOps")[0]
					disk_writeops_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_writeops_datapoints'] = json.dumps(disk_writeops_datapoints,default=date_handler)

					# DiskReadBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskReadBytes")[0]
					disk_readbytes_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_readbytes_datapoints'] = json.dumps(disk_readbytes_datapoints,default=date_handler)

					# DiskWriteBytes
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="DiskWriteBytes")[0]
					disk_writebytes_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['disk_writebytes_datapoints'] = json.dumps(disk_writebytes_datapoints,default=date_handler)
					
					# NetworkIn
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkIn")[0]
					networkin_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['networkin_datapoints'] = json.dumps(networkin_datapoints,default=date_handler)
					
					# NetworkOut
					metric = cloudwatch.list_metrics(dimensions={'InstanceId':instance.id}, metric_name="NetworkOut")[0]
					networkout_datapoints = metric.query(start, end, 'Average', '')
					instance_metrics['networkout_datapoints'] = json.dumps(networkout_datapoints,default=date_handler)

					aws_virtual_machines[instance.id] = instance_metrics


		vms_cache.vms_response = base64.b64encode(pickle.dumps(aws_virtual_machines, pickle.HIGHEST_PROTOCOL))	
		vms_cache.last_seen = timezone.now()
		vms_cache.is_updating = False
		vms_cache.save()
	
		print 'VMs cache was succesfully updated.'

	return HttpResponse("ALLDONE")
	

def aws_vm_view(request,vm_name):

	print '-- aws_vm_view'
	
	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
			
	user = request.user
	profile = userprofile.objects.get(user=request.user)
	user.last_login = datetime.datetime.now()
	user.save()

	ip = request.META['REMOTE_ADDR']
	_log_user_activity(profile,"click","/aws/"+vm_name,"aws_vm_view",ip=ip)


	vms_cache = Cache.objects.get(user=user)
	vm_cache =  vms_cache.vms_response
	vm_cache = base64.b64decode(vm_cache)
	try:
		vm_cache = pickle.loads(vm_cache)[vm_name]
	except:
		return HttpResponse("access denied")

	if(vm_cache['user_id']!=request.user.id):
		return HttpResponse("access denied")
		
	return render_to_response('aws_vm.html', {'vm_name':vm_name,'vm_cache':vm_cache,}, context_instance=RequestContext(request))


def ajax_virtual_machines(request):
	
	print '-- ajax virtual machines'
	
	if not request.user.is_authenticated():
		print 'anonymous'
		return HttpResponseRedirect("/")

	print request.user
	
	user = request.user
	profile = userprofile.objects.get(user=request.user)
	
	vms_cache = Cache.objects.get(user=user)
	vm_cache =  vms_cache.vms_response
	vm_cache = base64.b64decode(vm_cache)

	try:
		vm_cache = pickle.loads(vm_cache)
	except: vm_cache = {}


	example_response = { "i-61765f22":{"vmcolor":"lightBlue","vmtitle":"windows","averge":"0.0,0.33","state":"Running" }, \
		"i-75cf9e36":{"vmcolor":"lightBlue","vmtitle":"windows","averge":"13.56,15.0","state":"Running" }, \
		"i-d0705993":{"vmcolor":"orange","vmtitle":"windows","averge":"","state":"Stopped" } }

	
	c=0
	ajax_vms_response = "{"
	for vm in vm_cache:

		if(vm_cache[vm]["instance"]["state"]["state"].lower()!="terminated"):

			data_median = 0

			try:
				data = ""
				cpu_utilization_datapoints = vm_cache[vm]["cpu_utilization_datapoints"]
				cpu_utilization_datapoints = json.loads(cpu_utilization_datapoints)
				z=0
				for i in cpu_utilization_datapoints:
					data += str(i["Average"])
					try:
						data_median += float(i["Average"])
					except: pass

					if(len(cpu_utilization_datapoints)-1>z): 
						data += ","
					#print data
					z+=1
				try: 
					data_median = data_median/z
				except: data_median = 0 
			except:
				data = ""

			try: 
				instance_name = vm_cache[vm]["instance"]["tags"]["Name"]
			except: 
				instance_name = vm

			
			color = "silver"
			vm_state = vm_cache[vm]["instance"]["state"]["state"].title()
						
			if(vm_state=="Running"): 
				
				if(data_median<10):
					color = "green"
				if(data_median>10 and data_median<=25):
					color = "darkGreen"
				if(data_median>=25 and data_median<=50):
					color = "darkGreen"
				if(data_median>60 and data_median<=80):
					color = "lightOrange"
				if(data_median>80):
					color = "red"
				
			if(vm_state=="Stopped"): color = "black"
			if(vm_state=="Stopping"): color = "pink"
			if(vm_state=="Pending"): color = "pink"
			if(vm_state=="Shutting-Down"): color = "pink"
						
			ajax_vms_response += "\""
			ajax_vms_response += instance_name
			ajax_vms_response += "\": {"

			ajax_vms_response += "\"vmcolor\":\""
			ajax_vms_response += color
			ajax_vms_response += "\","

			ajax_vms_response += "\"vmtitle\":\""
			ajax_vms_response += "linux"
			ajax_vms_response += "\","
		
			ajax_vms_response += "\"averge\":\""
			ajax_vms_response += data
			ajax_vms_response += "\","

			ajax_vms_response += "\"state\":\""
			ajax_vms_response += vm_state
			ajax_vms_response += "\""

			ajax_vms_response += "},"

		if(c==len(vm_cache)-1):
			ajax_vms_response += "}"
			
		c+=1
		
		print '-_'*80
		print vm_cache[vm]["instance"]["state"]["state"].title(), vm

	ajax_vms_response = ajax_vms_response.replace(",}","}")
	
	return render_to_response('ajax_virtual_machines.html', {'user':user,'ajax_vms_response':ajax_vms_response,'vms_cached_response':vm_cache,}, context_instance=RequestContext(request))


def ajax_virtual_machines_box(request):
			
	return render_to_response('ajax_virtual_machines_box.html', locals(), context_instance=RequestContext(request))



