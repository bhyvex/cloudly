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




###### Devel Notes

Cloudly runs off of Hadoop and is powered by the OpenTSBD.  Please refer to the official OpenTSDB documentation for installation the instructions - http://opentsdb.net/docs/build/html/installation.html

<pre>
export JAVA_HOME=/usr

/opt/hbase-1.0.1.1/bin/start-hbase.sh

telnet 0 2181

env COMPRESSION=NONE HBASE_HOME=/opt/hbase-1.0.1.1/ /opt/opentsdb/tools/create_table.sh

/opt/opentsdb/bin/tsdb tsd --auto-metric --staticroot=/opt/opentsdb/static/ --port=4242 --auto-metric --cachedir="/home/hbase/opentsdb-cache/" --zkquorum=localhost:2181
</pre>
