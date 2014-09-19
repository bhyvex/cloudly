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

Enable utf-8 characters on the DB:
<pre>
mysql> use cloudly;
mysql> ALTER DATABASE cloudly charset=utf8;
mysql> ALTER TABLE userprofile_profile CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
</pre>

3) TBD

4) Install other python packages

<pre>
$ apt-get install python-dev 
$ apt-get install python-simplejson 
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

7) 

