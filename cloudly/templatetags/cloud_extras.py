import time
import json
import datetime

from django import template
register = template.Library()

from django.contrib.auth.models import User
from userprofile.models import Profile

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly

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


@register.filter(name="count_list")
def count_list(x):
	return len(x)	

@register.filter(name="times_hundred")
def times_hundred(x):
	return float(x)*100

@register.filter(name="times_hundred_rounded")
def times_hundred_rounded(x):
	return int(float(x)*100)


@register.filter(name='clear_filename')
def clear_filename(f):
	try:
		return str(f)[20:]
	except:
		return f


@register.filter(name='shorten_key')
def shorten_key(key):
	return key[:11]+'..'

	
@register.filter(name='get_file_extension')
def get_file_extension(f):
	return str(f).split('.')[-1:][0]


@register.filter(name='replace_dots')
def replace_dots(text):
	return text.replace(':','-')

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
	return x/1024/1000
	
	
@register.filter(name="clean_ps_command")
def clean_ps_command(command):

	command = command.replace('[','')
	command = command.replace(']','')
	
	if(command[-1:]==":"):
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

