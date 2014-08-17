from django.db import models

class UploadedFiles(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d')
