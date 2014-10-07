from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cache(models.Model):
	
	user = models.ForeignKey(User)
	
	# XXX Note: perhaps it's a good idea to work this on mongo?
	
	# vms_info1
	# vms_info2
	# vms_info3
	# vms_info4
	# vms_info5
	# vms_info6
	# vms_info7	
	# vms_info8

	last_seen = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now_add=True)
	