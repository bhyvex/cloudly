import re
import time
import json
import datetime
import base64, pickle

from django import template
register = template.Library()

from django.contrib.auth.models import User
from userprofile.models import Profile

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('mongo', 27017)

mongo = client.cloudly
from vms.models import Cache

def _seconds_since_epoch(d):

	date_time = d.isoformat().split('.')[0].replace('T',' ')
	pattern = '%Y-%m-%d %H:%M:%S'
	seconds_since_epoch = int(time.mktime(time.strptime(date_time, pattern)))

	return seconds_since_epoch


@register.filter(name='dict_get')
def dict_get(h, key):

	try: return h[key]
	except: pass
		
	return None

@register.filter(name='convert_disk_name')
def convert_disk_name(x):

    try: 
        return x.replace('/','slash')
    except: pass

    return None


@register.filter(name="count_list")
def count_list(x):
	return len(x)	

@register.filter(name="times_hundred")
def times_hundred(x):
	try:
		return float(x)*100
	except:
		return "error"

@register.filter(name="times_hundred_rounded")
def times_hundred_rounded(x):
	try:
		return int(float(x)*100)
	except:
		return "error"

@register.filter(name='clear_filename')
def clear_filename(f):
	try:
		return str(f)[20:]
	except:
		return f


@register.filter(name='shorten_key')
def shorten_key(key):
	return key[:11]+'..'

@register.filter(name='shorten_string')
def shorten_string(x,shorten):
	return x[:shorten]
	
@register.filter(name='get_file_extension')
def get_file_extension(f):
	return str(f).split('.')[-1:][0]


@register.filter(name='replace_dots')
def replace_dots(text):
	return text.replace(':','-')

@register.filter(name='make_float')
def make_float(value):
	return float(value)


@register.filter(name='make_json')
def make_json(json_):
	try:
		return json.loads(json_)
	except: return {}


@register.filter(name='make_json_sorted')
def make_json_sorted(json_):

	json_ = json.loads(json_)
	json_.sort(key=lambda json_: json_['Timestamp'])
	return json_

@register.filter(name='get_tags')
def get_tags(package):
	return Tags.objects.filter(package=package)

@register.filter(name='to_mb')
def to_mb(x):
	return long(x)/1024/1000
	
	
@register.filter(name="clean_ps_command")
def clean_ps_command(command):

	if(command[-1:]==":"):
		command = command[:-1]

	if(command[0]=="-"):
		command = command[1:]

	if(command[0]==" "):
		command = command[1:]
		
	command = command.replace('[','')
	command = command.replace(']','')

	command = command.replace('/usr/local/bin/','')
	command = command.replace('/usr/local/sbin/','')
	command = command.replace('/usr/bin/','')
	command = command.replace('/usr/sbin/','')
	command = command.replace('/bin/','')
	command = command.replace('/sbin/','')
	
	command = command.split(' ')[0]
	command = re.sub("([a-z|0-9]*)([A-Z][a-zA-Z]*)", "\\1 \\2", command)
	if(command[0]==" "): command = command[1:]
	
	command = command.split(' ')[0]

	return command

@register.filter(name="work_single_ps_command")
def work_single_ps_command(cmd):

	command = ""
	for i in cmd: command += i + " "
	command = command[:-1]

	return command

@register.filter(name='format_datetime_special')
def format_datetime_special(date):
	
	year = date.split('-')[0]
	month = date.split('-')[1]
	day = date.split('-')[2].split('T')[0]
	hour = date.split('-')[2].split('T')[1].split(':')[0]
	minute = date.split('-')[2].split('T')[1].split(':')[1]
	second = date.split('-')[2].split('T')[1].split(':')[2]
	
	return {'year':year, 'month':month, 'day':day, 'hour':hour, 'minute':minute, 'second':second}


@register.filter(name='count_user_servers')
def count_user_servers(user):
	
	try:
		vms_cache = Cache.objects.get(user=user)
		vms_response = vms_cache.vms_response
		vms_response = base64.b64decode(vms_response)
		vms_response = pickle.loads(vms_response)
		vms_cached_response = vms_response
	except: vms_cached_response = []

	return len(vms_cached_response)


@register.filter(name='count_user_files')
def count_user_files(user):
	
	#users_files_count = Uploaded_Files.objects.filter(user=user).count()
	users_files_count = 0
	
	return users_files_count

@register.filter(name='count_user_files_size')
def count_user_files_size(user):
	
	total_size = 0
	#for user_file in Uploaded_Files.objects.filter(user=user):
	#	total_size += user_file.size
	
	return total_size


@register.filter(name='get_server_activities')
def get_server_activities(server_uuid):
	activities = mongo.activity.find({'uuid':server_uuid,}).sort('_id',-1)
	return activities

@register.filter(name='substract_one')
def substract_one(x):
	x = int(x)
	return x-1

@register.filter(name='clean_percentage')
def clean_percentage(x):
	return str(x).replace('%','')
