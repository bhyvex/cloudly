Mongo Installation Instructions
-------------------------------

###### Install the MongoDB and its python connectors

<pre>
$ apt-get install mongodb
$ apt-get install python-pip
$ pip install pymongo
</pre>

###### Create MongoDB data directory

<pre>
$ sudo mkdir /data
$ sudo mkdir /data/db
</pre>

###### Set data directory to mongo configuration

Open mongo configuration file:

<pre>
$ sudo vim /etc/mongodb.conf
</pre>

Change:

<pre>
dbpath=/data/db
</pre>

###### Create db user for cloudly cb

<pre>
$ mongo
> use cloudly
> db.addUser({user:"cloudly",pwd:"cloudly",roles:["readWrite","dbAdmin"]})
> exit
</pre>

###### Run the MongoDB

<pre>
$ mongod
</pre>

