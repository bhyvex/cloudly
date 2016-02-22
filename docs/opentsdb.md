###### HBase + Hadoop + Zookeeper + OpenTSDB

Cloudly runs off of Hadoop and is powered by the OpenTSBD.  

First, you need to setup HBase.  If you are brand new to HBase and/or OpenTSDB we recommend you test with a stand-alone instance as this is the easiest to get up and running.

###### Install HBase

This guide describes the setup of a standalone HBase instance running against the local filesystem. This is not an appropriate configuration for a production instance of HBase, but will allow you to get up and running.

HBase requires that a JDK be installed.

<pre>
$ apt-get install openjdk-7-jdk
$ apt-get install openjdk-7-jre
</pre>

Choose a download site from this list of Apache Download Mirrors http://www.apache.org/dyn/closer.cgi/hbase/ and choose the file for Hadoop 2, which will be called something like hbase-0.98.13-hadoop2-bin.tar.gz).

Extract the downloaded file, and change to the newly-created directory.

<pre>
$ tar xzvf hbase-<?eval ${project.version}?>-bin.tar.gz
$ cd hbase-<?eval ${project.version}?>/
</pre>

For HBase 0.98.5 and later, you are required to set the JAVA_HOME environment variable before starting HBase.

<pre>
$ export JAVA_HOME=/usr
</pre>


Edit conf/hbase-site.xml, which is the main HBase configuration file. At this time, you only need to specify the directory on the local filesystem where HBase and ZooKeeper write data.

Example hbase-site.xml for Standalone HBase:

<pre>
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>file:///home/zookeeper/hbase</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/home/zookeeper/zookeeper</value>
  </property>
</configuration>
</pre>

You do not need to create the HBase data directory. HBase will do this for you. If you create the directory, HBase will attempt to do a migration, which is not what you want.


The bin/start-hbase.sh script is provided as a convenient way to start HBase. Issue the command, and if all goes well, a message is logged to standard output showing that HBase started successfully.

<pre>
$ bin/start-hbase.sh
</pre>

To test that this worked, connect to your running instance of HBase using the hbase shell command, located in the bin/ directory of your HBase install.

<pre>
$ telnet localhost 2181
Trying 127.0.0.1...
Connected to myhost.
Escape character is '^]'.
stats
Zookeeper version: 3.4.3-cdh4.0.1--1, built on 06/28/2012 23:59 GMT
Clients:
Latency min/avg/max: 0/0/677
Received: 4684478
Sent: 4687034
Outstanding: 0
Zxid: 0xb00187dd0
Mode: leader
Node count: 127182
Connection closed by foreign host.
</pre>

If you can't connect to Zookeeper, check IPs and name resolution. HBase can be finicky.

###### Install OpenTSDB

First off, install packages required for the OpenTSDB compilation:

<pre>
$ apt-get install autoconf
$ apt-get install gnuplot
</pre>

Download the latest version using git clone command or download a release from the site or Github. Then just run the build.sh script.

<pre>
$ git clone git://github.com/OpenTSDB/opentsdb.git opentsdb-install
$ cd opentsdb
$ ./build.sh
$ cd build
$ make install
</pre>

If compilation was successfuly, you should have a tsdb jar file in ./build along with a tsdb script. You can now execute command-line tool by invoking ./build/tsdb or you can run make install to install OpenTSDB on your system.


This is the first time that you are running OpenTSDB with your HBase instance, therefore you'd first need to create the necessary HBase tables.

<pre>
$ cd /usr/local/share/opentsdb
$ env COMPRESSION=NONE HBASE_HOME=/opt/hbase-1.1.3/ /opt/opentsdb/tools/create_table.sh
</pre>

The COMPRESSION value is either NONE, LZO, GZIP or SNAPPY. This will create four tables: tsdb, tsdb-uid, tsdb-tree and tsdb-meta.


Finally, start the OpenTSDB like so:

<pre>
/opt/opentsdb/bin/tsdb tsd --auto-metric --staticroot=/opt/opentsdb/static/ --port=4242 --auto-metric --cachedir="/home/hbase/opentsdb-cache/" --zkquorum=localhost:2181
</pre>

Installation includes an init script at /etc/init.d/opentsdb that can start, stop and restart OpenTSDB. Simply call service opentsdb start to start the tsd and service opentsdb stop to gracefully shutdown

At this point you have the OpenTSDB up and running. You can access the TSD's web interface through http://127.0.0.1:4242 (if it's running on your local machine).


And that's that!  :)
