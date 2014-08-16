#!/bin/sh
echo running development server
#python manage.py syncdb
python manage.py runserver 0.0.0.0:8000
