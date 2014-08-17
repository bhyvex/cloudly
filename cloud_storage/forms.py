from django import forms
from cloud_storage.models import UploadedFiles
  
class UploadFileForm(forms.ModelForm):

	class Meta:
		model = UploadedFiles


