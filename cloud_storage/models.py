from django.db import models

class UploadedFiles(models.Model):

    file = models.FileField(upload_to='%Y/%m/%d/%H:%M:%S')
	# XXX batch upload to the cloud
	# is_deployed = Boolean field.....
	