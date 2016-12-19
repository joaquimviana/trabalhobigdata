## Imports Necessários ao Cpython ##
from __future__ import print_function
import pandas as pd
import sys
import os
SPARK_HOME = os.environ["SPARK_HOME"]="/srv/spark"
PYTHONPATH=os.environ["PYTHONPATH"]= "/srv/spark/python/lib/py4j-0.8.2.1-src.zip:/srv/spark/spark/python"

## Adicionando o PYSPARK ao path ##
sys.path.append("/srv/spark/python/pyspark") 
sys.path.append("/srv/spark/python") 
sys.path.append("/srv/spark/python/lib/py4j") 
sys.path.append("/srv/spark/python/lib") 
sys.path.append("/srv/spark/python/pyspark/accumulators") 

## Import do Pyspark ##
from pyspark.sql import SparkSession


## Recebe os parametros dos Filtros ##
mesParam = config.loc[0,"mesParam"]
anoParam = config.loc[0,"anoParam"]
dominioParam = config.loc[0,"dominioParam"]

## Inicia a Sessao no master Local ##
spark = SparkSession\
    .builder\
    .appName("PythonQuery")\
    .getOrCreate()

##Carrega ods Dados para o RDD
lines = spark.read.csv('/home/joaquim/TrabalhoSpark/dados/PageViewsPerDayAll.csv')
## Organiza os dados
lines = lines.rdd.map(lambda row: [row[0],row[1].split("/")[0], row[1].split("/")[1], row[1].split("/")[2],row[2]])

## Faz a Seleção dos dados segundo os filtros
lines = lines.filter(lambda w: w[0] == dominioParam)
lines = lines.filter(lambda w: int(w[1]) == anoParam)
lines = lines.filter(lambda w: int(w[2]) == mesParam)

## Map (Dia / Qtd)
lines = lines.map(lambda x: (int(x[3]), int(x[4])))
##Agrega Qtd total / qtd
lines = lines.aggregateByKey((0,0), lambda a,b: (a[0] + b,    a[1] + 1), lambda a,b: (a[0] + b[0], a[1] + b[1]))

counts = lines.mapValues(lambda v: v[0]/v[1])
## Ordena dos dados pelo dia
counts = counts.sortBy(lambda a: a[0])
## Coleta os resultados
output = counts.collect()

## Salva o resultado em um Padas data frame
res = pd.DataFrame(output)

