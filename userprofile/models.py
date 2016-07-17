from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Activity(models.Model):

    user = models.ForeignKey(User)
    ip_addr = models.GenericIPAddressField(default="n/a")
    link = models.URLField(blank=True, verbose_name="links")
    activity = models.CharField(max_length=100, blank=True, verbose_name="activities", db_index=True)
    function = models.CharField(max_length=100, blank=True, verbose_name="function", db_index=True)
    meta = models.CharField(max_length=767, blank=True, verbose_name="meta", db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):

    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, blank=True, verbose_name="name", db_index=True)
    secret = models.CharField(max_length=100, blank=True, verbose_name="secret_key", db_index=True)
    agent_hash = models.CharField(max_length=20, blank=True, verbose_name="agent_hash", db_index=True)
    public_key = models.CharField(max_length=767, blank=True, verbose_name="public_key", db_index=True)
    public_key_passphrase = models.CharField(max_length=100, blank=True, verbose_name="ssh_passphrase", db_index=True)

    company = models.CharField(max_length=100, blank=True, verbose_name="company")
    company_url = models.CharField(max_length=100, blank=True, verbose_name="custom_url")

    skills = models.CharField(max_length=512, blank=True, verbose_name="skills", db_index=True)
    country = models.CharField(max_length=10, blank=True, verbose_name="country", db_index=True)
    language = models.CharField(max_length=10, blank=True, verbose_name="language", db_index=True)

    picture = models.URLField(blank=True, verbose_name="User Avatar / Company Logo")
    twitter = models.CharField(max_length=75, blank=True)

    mobile = models.CharField(max_length=20, blank=True, verbose_name="mobile_number_1")

    street_address_1 = models.CharField(max_length=100, blank=True, verbose_name="street_address_1")
    street_address_2 = models.CharField(max_length=100, blank=True, verbose_name="street_address_2")
    street_address_3 = models.CharField(max_length=100, blank=True, verbose_name="street_address_3")

    email_notifications = models.BooleanField(default=True)
    twitter_notifications = models.BooleanField(default=False)

    aws_access_key = models.CharField(max_length=100, blank=True, verbose_name="Access Key", db_index=True)
    aws_secret_key = models.CharField(max_length=100, blank=True, verbose_name="Secret Key", db_index=True)
    aws_enabled_regions = models.CharField(max_length=256, default="us-west-1,us-west-2,us-east-1,eu-west-1", verbose_name="Regions", db_index=True)
    aws_ec2_verified = models.BooleanField(default=False)
    aws_s3_verified = models.BooleanField(default=False)
    aws_cloudfront_verified = models.BooleanField(default=False)
    aws_automatic_backups = models.BooleanField(default=False)

    oauth_token = models.CharField(max_length=100, blank=True, verbose_name="Token", db_index=True)
    oauth_secret = models.CharField(max_length=100, blank=True, verbose_name="Secret", db_index=True)

    pricing_plan = models.IntegerField(default=0)

    clicks = models.IntegerField(default=0)
    first_login = models.BooleanField(default=False)
