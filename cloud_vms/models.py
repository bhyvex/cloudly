from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cache(models.Model):
	
	user = models.ForeignKey(User)
	
	# XXX Note: perhaps it's a good idea to work this on mongo?
	
	# vms_detail_level1
	# vms_detail_level2
	# vms_detail_level3
	# vms_detail_level4
	# vms_detail_level5
	
	last_seen = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now_add=True)
	