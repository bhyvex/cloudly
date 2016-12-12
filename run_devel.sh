#!/bin/sh

#clear

#echo !! Synchronizing the database..
#python manage.py syncdb

#echo
#echo !! Updating to the latest version from git....
#git pull

echo
echo !! Running development server..
python manage.py runserver 0.0.0.0:8080
