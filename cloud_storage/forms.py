from django import forms
from cloud_storage.models import Files
  
class UploadFileForm(forms.ModelForm):

	class Meta:
		model = Files

