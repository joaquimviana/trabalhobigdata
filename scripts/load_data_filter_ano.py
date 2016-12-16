from __future__ import print_function
import pandas as pd
import sys
import os
SPARK_HOME = os.environ["SPARK_HOME"]="/srv/spark"
PYTHONPATH=os.environ["PYTHONPATH"]= "/srv/spark/python/lib/py4j-0.8.2.1-src.zip:/srv/spark/spark/python"


sys.path.append("/srv/spark/python/pyspark") 
sys.path.append("/srv/spark/python") 
sys.path.append("/srv/spark/python/lib/py4j") 
sys.path.append("/srv/spark/python/lib") 
sys.path.append("/srv/spark/python/pyspark/accumulators") 
from operator import add
from pyspark.sql import SparkSession

spark = SparkSession\
    .builder\
    .appName("PythonQuery")\
    .getOrCreate()

lines = spark.read.csv('/home/joaquim/TrabalhoSpark/dados/PageViewsPerDayAll.csv')

lines = lines.rdd.map(lambda row: [row[0],row[1].split("/")[0], row[1].split("/")[1], row[1].split("/")[2],row[2]])

counts = lines.map(lambda x: (int(x[1]), 1)).reduceByKey(add)

counts = counts.sortBy(lambda a: -a[0])

output = counts.collect()

for (day, count) in output:
    print("%s: %i" % (day, count))


res = pd.DataFrame(output)

