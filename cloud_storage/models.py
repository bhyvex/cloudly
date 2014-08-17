from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Files(models.Model):
	file = models.FileField(upload_to='%Y/%m/%d/%H:%M:%S')
	
class Uploaded_Files(models.Model):
	
	user = models.OneToOneField(User)
	file = models.ForeignKey(Files)
	is_deployed = models.BooleanField(default=False)
