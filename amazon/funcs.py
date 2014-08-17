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

def aws_instance_start(name):

	try:
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].start()
	except: pass
	
	return False


def aws_instance_stop(name):
	
	try:
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].stop()
	except: pass
	
	return False


def aws_instance_reboot(name):

	try:
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].reboot()
	except: pass
	
	return False

def aws_instance_terminate(name):

	try:
		aws_conn = boto.ec2.connect_to_region("us-west-2",aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].terminate()
	except: pass
	
	return False
