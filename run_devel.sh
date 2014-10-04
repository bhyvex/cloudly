#!/bin/sh
echo running development server
#python manage.py syncdb
git pull
python manage.py runserver 0.0.0.0:8000
