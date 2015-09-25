#!/opt/anaconda/bin/python
import sys, os
import subprocess
import time
from cm_api.api_client import ApiResource

#print "Restart Cloudera Manager..."
#subprocess.call("sudo service cloudera-scm-agent restart", shell=True)

# Get a handle to the API client
for i in range(0,15):
    while True:
        try:
            cm_host = "127.0.0.1"
            api = ApiResource(cm_host, username="admin", password="admin")
            cdh=api.get_all_clusters()[0]
        except:
            print "Failed to connect to Cloudera Manager."
            print "Attempting to connect to Cloudera Manager..."
            time.sleep(15)
            continue
        break

print "Restarting HDFS..."
hdfs=cdh.get_service('hdfs')
cmd = hdfs.restart().wait()
print "HDFS Restart: " + ("Success" if cmd.success else "Fail")
print "Restarting YARN..."
yarn=cdh.get_service('yarn')
cmd = yarn.restart().wait()
print "YARN Restart: " + ("Success" if cmd.success else "Fail") 
print "Restarting Zookeeper..."
zk=cdh.get_service('zookeeper')
cmd = zk.restart().wait()
print "Zookeeper Restart: " + ("Success" if cmd.success else "Fail") 
print "Restarting Hive..."
hive=cdh.get_service('hive')
cmd = hive.restart().wait()
print "Hive Restart: " + ("Success" if cmd.success else "Fail") 
print "Restarting Impala..."
imp=cdh.get_service('impala')
cmd = imp.restart().wait()
print "Impala Restart: " + ("Success" if cmd.success else "Fail") 
print "Restarting Spark..."
spark=cdh.get_service('spark_on_yarn')
cmd = spark.restart().wait()
print "Spark Restart: " + ("Success" if cmd.success else "Fail") 
print "Restarting HUE..."
hue=cdh.get_service('hue')
cmd = hue.restart().wait()
print "HUE Restart: " + ("Success" if cmd.success else "Fail") 

# Ingest Data
print "Ingesting data..."
subprocess.call("/home/cloudera/tree/script/00_data_ingest.sh", shell=True)

# Start ipython notebook
print "Starting ipython notebook..."
subprocess.call("sudo nohup /opt/anaconda/bin/ipython notebook --profile=pyspark > /dev/null 2>&1&", shell=True)
print "Done! View Tree Analysis by navigating to http://localhost:8890"
