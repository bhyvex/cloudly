#!/bin/sh
echo copying Tomas\' custom settings
cp -f cloudly/settings.py-kamil cloudly/settings.py 

echo running development server

python manage.py syncdb
python manage.py runserver 0.0.0.0:8000
