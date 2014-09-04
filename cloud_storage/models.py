from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Files(models.Model):
	file = models.FileField(upload_to='%Y/%m/%d/%H:%M:%S')
	
class Uploaded_Files(models.Model):
	
	user = models.ForeignKey(User)
	file = models.ForeignKey(Files)
	
	name = models.CharField(max_length=512, blank=True)
	
	#name_slug = models.SlugField(max_length=767, blank=True)
	share_link = models.URLField(blank=True)

	#is_private = models.BooleanField(default=False)
	#private_link = models.URLField(blank=True)
	is_passwd_protected = models.BooleanField(default=False)
	
	is_deployed = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	is_shared = models.BooleanField(default=False)
	
	date_created = models.DateTimeField(auto_now_add=True)
