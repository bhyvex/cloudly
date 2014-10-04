#!/bin/sh

clear

echo ** Synchronizing the database..
python manage.py syncdb

sleep 1

echo
echo ** Updating to the latest version from git....
git pull

sleep 1

echo
echo ** Running development server..
python manage.py runserver 0.0.0.0:8000

