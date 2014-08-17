# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch





########################################################
## TODO expand these funcs with the Region parameter!!!!
########################################################

def aws_instance_start(request, name):

	try:
		aws = AWS.objects.get(user=request.user)
		AWS_ACCESS_KEY=aws.AWS_ACCESS_KEY
		AWS_ACCESS_SECRET=aws.AWS_SECRET_KEY
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].start()
	except: pass
	
	return HttpResponseRedirect('/')


def aws_instance_stop(request, name):
	
	try:
		aws = AWS.objects.get(user=request.user)
		AWS_ACCESS_KEY=aws.AWS_ACCESS_KEY
		AWS_ACCESS_SECRET=aws.AWS_SECRET_KEY	
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].stop()
	except: pass
	
	return HttpResponseRedirect('/')


def aws_instance_reboot(request, name):

	try:
		aws = AWS.objects.get(user=request.user)
		AWS_ACCESS_KEY=aws.AWS_ACCESS_KEY
		AWS_ACCESS_SECRET=aws.AWS_SECRET_KEY
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].reboot()
	except: pass
	
	return HttpResponseRedirect('/')

def aws_instance_terminate(request, name):

	try:
		aws = AWS.objects.get(user=request.user)
		AWS_ACCESS_KEY=aws.AWS_ACCESS_KEY
		AWS_ACCESS_SECRET=aws.AWS_SECRET_KEY
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].terminate()
	except: pass
	
	return HttpResponseRedirect('/')
