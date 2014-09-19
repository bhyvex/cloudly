Cloudly
=======

Installation Instructions
-------------------------

1) Install MySQL server and Python MySQLdb

<pre>
$ apt-get install mysql-server python-mysqldb
</pre>

Optionally configure your MySQL server to meet your specific requirements.

As for the user/password, this one needs to match the cloudly/cloudly/settings.py.

2) Create Cloudly Database

<pre>
$ mysql -u root -p
mysql> create database cloudly;
</pre>


4) Install other python packages

<pre>
$ apt-get install python-dev 
$ apt-get install python-simplejson 
$ apt-get install python-django
</pre>

5) Install MongoDB and it's python connector

<pre>
apt-get install mongodb
apt-get install python-pymongo
</pre>

..and configure your server to meet your requirements.

6) Download the latest version of Cloudly

<pre>
git clone https://github.com/jparicka/cloudly.git cloudly
</pre>

7) Create Cloudly ORM database tables

<pre>
$ cd cloudly
$ python manage.py syncdb
</pre>

If you get an error saying "Access denied for user 'root'@'localhost" then you'd need to edit the cloudly/settings.py and setup the DB section accordingly to your present DB settings.

Assuming this operation succeded, Django will answer the following:

<pre>
You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): 
</pre>

Answer "no" to this question.


8) Enable utf-8 characters on the database

<pre>
$ mysql -u root -p
mysql> use cloudly;
mysql> ALTER DATABASE cloudly charset=utf8;
mysql> ALTER TABLE userprofile_profile CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
</pre>

9) Install Amazon Boto - Python Interface to Amazon Web Services

<pre>
$ apt-get install python-boto
</pre>

10) Run MongoDB

<pre>
$ sudo mkdir /data
$ sudo mkdir /data/db
$ mongod &
</pre>

..and configure your server to meet your requirements.
