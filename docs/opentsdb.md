###### Install HBase + Hadoop + Zookeeper + OpenTSDB

Cloudly runs off of Hadoop and is powered by the OpenTSBD.  

First, you need to setup HBase.  If you are brand new to HBase and/or OpenTSDB we recommend you test with a stand-alone instance as this is the easiest to get up and running.

###### Install HBase

This guide describes the setup of a standalone HBase instance running against the local filesystem. This is not an appropriate configuration for a production instance of HBase, but will allow you to experiment with HBase.






###### Devel Notes

Cloudly runs off of Hadoop and is powered by the OpenTSBD.  Please refer to the official OpenTSDB documentation for installation the instructions - http://opentsdb.net/docs/build/html/installation.html

<pre>
export JAVA_HOME=/usr

/opt/hbase-1.0.1.1/bin/start-hbase.sh

telnet 0 2181

env COMPRESSION=NONE HBASE_HOME=/opt/hbase-1.0.1.1/ /opt/opentsdb/tools/create_table.sh

/opt/opentsdb/bin/tsdb tsd --auto-metric --staticroot=/opt/opentsdb/static/ --port=4242 --auto-metric --cachedir="/home/hbase/opentsdb-cache/" --zkquorum=localhost:2181
</pre>
