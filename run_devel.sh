#!/bin/sh

#echo syncing db
#python manage.py syncdb

#echo
echo updating from git....
git pull

echo
echo running development server..
python manage.py runserver 0.0.0.0:8000
