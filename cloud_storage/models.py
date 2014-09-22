from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Files(models.Model):
	file = models.FileField(upload_to='%Y/%m/%d/%H:%M:%S')
	
class Uploaded_Files(models.Model):
	
	user = models.ForeignKey(User)
	file = models.ForeignKey(Files)
	
	name = models.CharField(max_length=512, blank=True)
	size = models.IntegerField(blank=True)
	file_type = models.CharField(max_length=10, blank=True)
	
	thumbnail_pic1 = models.URLField(blank=True)
	thumbnail_pic2 = models.URLField(blank=True)
	thumbnail_pic3 = models.URLField(blank=True)
	
	is_deployed = models.BooleanField(default=False)
	is_shared = models.BooleanField(default=False)
	
	share_link = models.URLField(blank=True)
	share_link_clicks_count = models.IntegerField(default=0)
	#share_link_password = 
	
	is_deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)
