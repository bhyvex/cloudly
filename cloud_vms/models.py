from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cache(models.Model):
	
	user = models.ForeignKey(User)
	
	# vms_respose
	# vms_info_filtered_1

	last_seen = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now_add=True)
	