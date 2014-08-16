from django.db import models
from django.contrib.auth.models import User

import base64
try:
	import cPickle as pickle
except:
	import pickle
 
class SerializedDataField(models.TextField):

	__metaclass__ = models.SubfieldBase
 
	def to_python(self, value):
		if value is None: return
		if not isinstance(value, basestring): return value
		value = pickle.loads(base64.b64decode(value))
		return value
 
	def get_db_prep_save(self, value):
		if value is None: return
		return base64.b64encode(pickle.dumps(value))

class Tag(models.Model):
	
	name = models.CharField(max_length=50)
	name_slug = models.SlugField(max_length=200, blank=True)
	name_slug_before_unique = models.SlugField(max_length=200, blank=True)
	
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):

		if not self.name_slug:
			from django.template.defaultfilters import slugify
			potential_slug = slugify(self.name)
			name_slug_before_unique = potential_slug
			if Tag.objects.filter(name_slug=potential_slug).count() > 0:
				# slug is already in use
				check_for_same = Tag.objects.filter(name_slug_before_unique=potential_slug).order_by('-pk')[:1]
				if len(check_for_same) > 0:
					# add +1 to previous slug
					previous_number = check_for_same[0].name_slug.split('-')[-1]
					new_number = int(previous_number) + 1
					name_slug = potential_slug + '-' + str(new_number)
				else:
					name_slug = potential_slug + '-1'
			else:
				name_slug = potential_slug
				name_slug_before_unique = ''
		
			self.name_slug = name_slug
			self.name_slug_before_unique = name_slug_before_unique

		super(Tag, self).save(*args, **kwargs)


class packages(models.Model):
	
	title = models.CharField(max_length=250)
	description = models.TextField()
	package_name = models.CharField(max_length=250)
	package_link = models.URLField()
	package_ami = models.CharField(max_length=20)
	icon = models.URLField()


class tags(models.Model):
	
	tag = models.ForeignKey(Tag)
	package = models.ForeignKey(packages)
