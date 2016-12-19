## Imports Necessários ao Cpython ##
from __future__ import print_function
import pandas as pd
from operator import add
import sys
import os

## Adicionando o PYSPARK ao path ##
SPARK_HOME = os.environ["SPARK_HOME"]="/srv/spark"
PYTHONPATH=os.environ["PYTHONPATH"]= "/srv/spark/python/lib/py4j-0.8.2.1-src.zip:/srv/spark/spark/python"
sys.path.append("/srv/spark/python/pyspark") 
sys.path.append("/srv/spark/python") 
sys.path.append("/srv/spark/python/lib/py4j") 
sys.path.append("/srv/spark/python/lib") 
sys.path.append("/srv/spark/python/pyspark/accumulators") 

## Import do Pyspark ##
from pyspark.sql import SparkSession


## Inicia a Sessao no master Local ##
spark = SparkSession\
    .builder\
    .appName("PythonQuery")\
    .getOrCreate()

##Carrega ods Dados
lines = spark.read.csv('/home/joaquim/TrabalhoSpark/dados/PageViewsPerDayAll.csv')
## Organiza os dados
lines = lines.rdd.map(lambda row: [row[0],row[1].split("/")[0], row[1].split("/")[1], row[1].split("/")[2],row[2]])

counts = lines.map(lambda x: (x[0], -int(x[4]))).reduceByKey(add)

counts = counts.sortBy((lambda a: a[1]))

output = counts.collect()

res = pd.DataFrame(output)

