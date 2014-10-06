from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cache(models.Model):
	
	user = models.ForeignKey(User)
	
	# detail_level1
	# detail_level2
	# detail_level3
	
	last_seen = models.DateTimeField(auto_now_add=True)
	date_created = models.DateTimeField(auto_now_add=True)
	