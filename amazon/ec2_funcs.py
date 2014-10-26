# -*- coding: utf-8 -*-

import os
import time
import pickle
import logging
import datetime

logger = logging.getLogger(__name__)

import boto.ec2
import boto.ec2.cloudwatch


def aws_instance_start(name, region):

	try:
		aws_conn = boto.ec2.connect_to_region(region,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].start()
	except: pass
	
	return False


def aws_instance_stop(name, region):
	
	try:
		aws_conn = boto.ec2.connect_to_region(region,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].stop()
	except: pass
	
	return False


def aws_instance_reboot(name, region):

	try:
		aws_conn = boto.ec2.connect_to_region(region,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].reboot()
	except: pass
	
	return False

def aws_instance_terminate(name, region):

	try:
		aws_conn = boto.ec2.connect_to_region(region,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_ACCESS_SECRET)
		instance = aws_conn.get_all_instances(instance_ids=[name,])
		instance[0].instances[0].terminate()
	except: pass
	
	return False
