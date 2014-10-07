from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cache(models.Model):
	
	user = models.ForeignKey(User)
	vms_respose = models.TextField(blank=True)

	vms_info_filtered_1 = models.TextField(blank=True)
	vms_info_filtered_2 = models.TextField(blank=True)
	vms_info_filtered_3 = models.TextField(blank=True)
	vms_info_filtered_4 = models.TextField(blank=True)
	vms_info_filtered_5 = models.TextField(blank=True)

	last_seen = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now_add=True)
