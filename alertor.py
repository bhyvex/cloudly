# -*- coding: utf-8
#!/usr/bin/env python

import os
import time
import tweepy
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudly.settings")
django.setup()

from profiles.models import Profile
from django.contrib.auth.models import User

if __name__ == "__main__":
    print "hello world from alertor"
