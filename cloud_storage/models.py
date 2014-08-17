from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UploadedFiles(models.Model):

	file = models.FileField(upload_to='%Y/%m/%d/%H:%M:%S')
	user = models.OneToOneField(User)
	
	# XXX batch upload to the cloud
	# is_deployed = Boolean field.....
	