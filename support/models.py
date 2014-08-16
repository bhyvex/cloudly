import base64
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

try:
	import cPickle as pickle
except:
	import pickle

from invoices.models import Invoice	

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


class Messages(models.Model):
	
	owner = models.ForeignKey(User,related_name="owner")	
	ticket_title = models.CharField(max_length=400, blank=True, db_index=True)
	ticket_text = models.TextField(blank=True, db_index=True)
	
	pay_amount = models.IntegerField(default=0)
	paid = models.BooleanField(default=False)
	#invoice = models.ForeignKey(Invoice, related_name="invoice", null=True)
	
	ticket_slug = models.SlugField(max_length=200, blank=True)
	ticket_slug_before_unique = models.SlugField(max_length=200, blank=True)

	answered_by = models.ForeignKey(User,related_name="answered_by")
	date_answered = models.DateTimeField(null=True)
	answers_count = models.IntegerField(default=0)

	date_seen_by_owner = models.DateTimeField(null=True)
	date_seen_by_admin = models.DateTimeField(null=True)
	
	is_favorited = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	is_closed = models.BooleanField(default=False)
	
	date_added = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):

		if not self.ticket_slug:
			from django.template.defaultfilters import slugify
			potential_slug = slugify(self.ticket_title)
			ticket_slug_before_unique = potential_slug
			if Messages.objects.filter(ticket_slug=potential_slug).count() > 0:
				# slug is already in use
				check_for_same = Messages.objects.filter(ticket_slug_before_unique=potential_slug).order_by('-pk')[:1]
				if len(check_for_same) > 0:
					# add +1 to previous slug
					previous_number = check_for_same[0].ticket_slug.split('-')[-1]
					new_number = int(previous_number) + 1
					ticket_slug = potential_slug + '-' + str(new_number)
				else:
					ticket_slug = potential_slug + '-1'
			else:
				ticket_slug = potential_slug
				ticket_slug_before_unique = ''
		
			self.ticket_slug = ticket_slug
			self.ticket_slug_before_unique = ticket_slug_before_unique

		super(Messages, self).save(*args, **kwargs)


class Answers(models.Model):

	user = models.ForeignKey(User)
	answer_text = models.TextField(blank=True, db_index=True)
	related_message = models.ForeignKey(Messages)
	date_added = models.DateTimeField(auto_now_add=True)
