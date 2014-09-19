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


2) Install other python packages

<pre>
$ apt-get install python-dev 
$ apt-get install python-simplejson 
</pre>

3) Install MongoDB and it's python connector

<pre>
apt-get install mongodb
apt-get install python-pymongo
</pre>

..and configure your server to meet your requirements.

4) Download the latest version of Cloudly

<pre>
git clone https://github.com/jparicka/cloudly.git cloudly
</pre>

5) 

