#/usr/bin/env bash

# Script in support for loading data if necessary
if hadoop fs -test -d /user/cloudera/german ; then
    echo "Data already loaded, moving on."
else
    # Load file into hdfs
    hdfs dfs -mkdir /user/cloudera/german
    hdfs dfs -put /home/cloudera/tree/data/german_credit.csv /user/cloudera/german/
    # Run hive script to create table on text file and a copy in parquet
    hive -f /home/cloudera/tree/script/00_create_tables.hql
    # ensure that table is accessible in impala
    impala-shell -q 'invalidate metadata default.german'
    impala-shell -q 'invalidate metadata default.german_parquet'
fi





