import time
import datetime

from django import template
register = template.Library()

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile

import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient('localhost', 27017)

mongo = client.cloudly

from django.contrib.auth.models import User
from userprofile.models import Profile as userprofile

from cloud_software.models import Packages
from cloud_software.models import Tags, Tag

def _seconds_since_epoch(d):

	date_time = d.isoformat().split('.')[0].replace('T',' ')
	pattern = '%Y-%m-%d %H:%M:%S'
	seconds_since_epoch = int(time.mktime(time.strptime(date_time, pattern)))

	return seconds_since_epoch

@register.filter(name='dict_get')
def dict_get(h, key):

	try:
		return h[key]
	except: pass
		
	return None

@register.filter(name='replace_dots')
def replace_dots(text):
	return text.replace(':','-')


@register.filter(name='get_tags')
def get_tags(package):
	return Tags.objects.filter(package=package)

@register.filter(name='get_server_activities')
def get_server_activities(server_uuid):

	activities = mongo.activity.find({'uuid':server_uuid,}).sort('_id',-1)

	return activities

