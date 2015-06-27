Cloudly
=======

Project Cloudly is "The Easiest To Setup" software to Monitor and to control your servers.  It's a first line of defence for your servers and also the ultimate Management Dashboard for your Cloud.
It saves you money and the energies by taking away most of the usual servers monitoring complexities allowing you to focus more on control and better use of your infrastructure. 

Cloudly can scale to writing millions of data per 'second' on commodity servers with regular spinning hard drives.  This is due and thanks to the technologies it utilises (e.g. OpenTSDB to begin with).

Cloudly is fully automated and does the servers monitoring for you with close to nothing to setup.



Installation Instructions
-------------------------

###### Install MySQL server and Python MySQLdb

<pre>
$ apt-get install mysql-server python-mysqldb
</pre>

Optionally configure your MySQL server to meet your specific requirements.

As for the user/password, this one needs to match the entries in the cloudly/cloudly/settings.py file.

###### Create the project database

<pre>
$ mysql -u root -p
mysql> create database cloudly;
</pre>


###### Install various python modules

<pre>
$ apt-get install python-dev 
$ apt-get install python-django
$ apt-get install python-openssl
</pre>


###### Install the MongoDB and it's python connectors

<pre>
$ apt-get install mongodb
$ apt-get install python-pip
$ pip install pymongo
</pre>

..and configure your server to meet your specific requirements.

###### Download the latest version of the Cloudly Project from github

<pre>
$ apt-get install git
$ sudo adduser cloudly
$ su - cloudly
$ git clone https://github.com/jparicka/cloudly.git cloudly
</pre>

###### Create the ORM database tables

<pre>
$ cd cloudly
$ python manage.py syncdb
</pre>

If you get an error saying "Access denied for user 'root'@'localhost" then you'd need to edit the cloudly/settings.py and setup the DB section accordingly to your present DB settings.

Assuming this operation succeded, Django will ask you the following:

<pre>
You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): no
</pre>

Answer "no" to this question.


###### Enable Unicode on the database

<pre>
$ mysql -u root -p
mysql> use cloudly;
mysql> ALTER DATABASE cloudly charset=utf8;
mysql> ALTER TABLE userprofile_profile CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
</pre>

###### Install Amazon Boto - Python Interface to Amazon Web Services

<pre>
$ apt-get install python-boto
</pre>

###### Run the MongoDB

<pre>
$ sudo mkdir /data
$ sudo mkdir /data/db
$ mongod
</pre>

..and configure your server to meet your specific requirements.

###### Run the development server

At this point you should be able to run the administration dashboard (Django App):

<pre>
$ echo Never run this as user root!
$ ./run_devel.sh
</pre>

Now that you have the User Interface (Admin Dashboard) up and running you'd need to get the API started.  You can do so by following the instructions in the next step.


###### Run the API

API server runs off of Flask therefore you'd need to install Python Flask first.  To do so simply copy and paste the following into your terminal window:

<pre>
$ apt-get install python-flask
</pre>

Once you have the Flask installed, simply run the API like so:

<pre>
$ python api.py
</pre>


###### (optional) Configure the web server (NGINX without the SSL support)

First and foremost install the NGINX (and Python Flup module), like so:

<pre>
$ apt-get install nginx
$ apt-get install python-flup
</pre>

Open up your NGINX config file:

<pre>
$ vi /etc/nginx/nginx.conf
</pre>

..and paste in the following configuration:

<pre>
user cloudly cloudly;
worker_processes  2;

error_log /var/log/nginx/error_log info;

events {
    worker_connections  1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main
        '$remote_addr - $remote_user [$time_local]'
        '"$request" $status $bytes_sent'
        '"$http_referer" "$http_user_agent"'
        '"$gzip_ratio"';

    gzip on;
    gzip_min_length 1100;
    gzip_buffers 4 8k;
    gzip_types text/plain;
    output_buffers 1 32k;
    postpone_output 1460;
    sendfile on;
    tcp_nopush  on;
    tcp_nodelay on;
    keepalive_timeout 75 20;
    ignore_invalid_headers on;
    index index.xhtml;

    client_header_timeout 10m;
    client_body_timeout 10m;
    send_timeout 10m;
    connection_pool_size 256;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 2k;
    request_pool_size 4k;

    server {
        listen 80;
        server_name projectcloudly.com;
        location /site_media  {
            alias /static/;
            }
        location ~* ^.+\.(jpg|jpeg|gif|png|ico|css|zip|tgz|gz|rar|bz2|doc|xls||pdf|js|counters) {
            access_log   off;
            expires      30d; 
            }
        location / {
            fastcgi_pass 127.0.0.1:8080;
            fastcgi_param SERVER_ADDR $server_addr;
            fastcgi_param SERVER_PORT $server_port;
            fastcgi_param SERVER_NAME $server_name;
            fastcgi_param SERVER_PROTOCOL $server_protocol;
            fastcgi_param PATH_INFO $fastcgi_script_name;
            fastcgi_param REQUEST_METHOD $request_method;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_param CONTENT_TYPE $content_type;
            fastcgi_param CONTENT_LENGTH $content_length;
            fastcgi_pass_header Authorization;
            fastcgi_param REMOTE_ADDR $remote_addr;
            fastcgi_param X_FORWADRD_FOR $proxy_add_x_forwarded_for;
            fastcgi_intercept_errors off;
            }
        access_log  /var/log/nginx/cloudly.access_log main;
        error_log   /var/log/nginx/cloudly.error_log;
        }
    }
</pre>

Great! Now you should be able to run the NGINX server using the WSGI protocol on your very own server (effectively a Django server with the MySQL for the user data and Mongodb for the graphs/logging DB).

For more information about the Django and NGINX configuration see the NGINX Wiki on <a>http://wiki.nginx.org/DjangoFastCGI</a>

For information about the MongoDB visit <a>http://www.mongodb.org/</a>

DB Backends
-----------

On Cloudly, we utilize Redis primarily to store web sesssions data.

###### Install Redis

To get the Redis up and running on your system, simply pull it off of your distro repo..

<pre>
$ sudo apt-get install redis-server
$ redis-server --version
Redis server v=2.8.4 malloc=jemalloc-3.4.1 bits=64 build=a44a05d76f06a5d9
</pre>

###### Configure Redis to connect over a socket

You can connect to a local Redis instance over the network layer (TCP to the loopback interface) or through a unix socket file.

In order to avoid the small overhead of TCP, we can configure Redis to accept direct socket connections. To do this, edit your /etc/redis/redis.conf file, comment out the bind and port directives and uncomment the two unixsocket directives.

Once you've done that, your redis.conf file should look something like this - 

<pre>
# Accept connections on the specified port, default is 6379.
# If port 0 is specified Redis will not listen on a TCP socket.
# port 6379
# If you want you can bind a single interface, if the bind option is not
# specified all the interfaces will listen for incoming connections.
#
# bind 127.0.0.1
# Specify the path for the unix socket that will be used to listen for
# incoming connections. There is no default, so Redis will not listen
# on a unix socket when not specified.
#
unixsocket /var/run/redis/redis.sock
unixsocketperm 777
</pre>

After making changes to its configuration you will need to restart Redis:

<pre>
$ sudo service redis-server restart
</pre>

You can now check if Redis is up and accepting connections:

<pre>
$ redis-cli ping
PONG
</pre>

Finally, install the python-redis and django-redis bindings, like so:

<pre>
$ sudo pip install redis
$ sudo pip install django-redis-cache
$ sudo pip install django-redis-sessions
</pre>


###### Install OpenTSDB

Install the OpenTSDB as per http://opentsdb.net/docs/build/html/installation.html

This will enable goodies such as Hadoop, HBase from Apache and first and foremost the almighty OpenTSDB!  :)


..and that's that!  :)

Enjoy!


Screenshots & Live Demo
-----------------------

![alt screen0](https://raw.githubusercontent.com/jparicka/cloudly/master/static/screenshots/screenshot0.png)

![alt screen1](https://raw.githubusercontent.com/jparicka/cloudly/master/static/screenshots/screenshot1.png)

###### Demo

Project can be currently seen on https://

