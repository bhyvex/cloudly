from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Invoice(models.Model):
	
	user = models.ForeignKey(User)
	product = models.CharField(max_length=100,default='', verbose_name="products")
	items = models.CharField(max_length=300,default='', verbose_name="items")
	total = models.IntegerField(default=0)
	payed = models.IntegerField(default=0)
	date_created = models.DateTimeField(auto_now_add=True)
	paypal_response_json = models.TextField(default='')
	paypal_confirmation_json = models.TextField(default='')
