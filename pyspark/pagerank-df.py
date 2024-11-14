
import findspark


from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

import re
import sys
from operator import add
from typing import Iterable, Tuple

from pyspark.resultiterable import ResultIterable

from pyspark.sql import Window
from pyspark.sql.functions import sum as sql_sum


import os

if __name__ == "__main__":
    partitionBy = sys.argv[4].lower() == "true"

    # Helper function to conditionally apply partitioning
    def apply_partitioning(df, column_name):
        return df.repartition(column_name) if partitionBy else df

    findspark.init()

    # Créez une session Spark
    spark = SparkSession.builder.appName("PageRankExample").getOrCreate()

    schema = StructType([
        StructField("source", StringType(), nullable=True),
        StructField("predicate", StringType(), nullable=True),
        StructField("target", StringType(), nullable=True)
    ])

    # Chargez vos données web en tant que DataFrame
    # Supposons que vous ayez un DataFrame avec deux colonnes : 'source' et 'target' représentant les liens entre les pages web
    # Par exemple, vous pouvez le charger à partir d'un fichier CSV
    data = spark.read.option("delimiter"," ").csv(sys.argv[1], header=False, schema=schema)
    data.show(5,truncate=200)

    # So we can really write SQL !!
    data.createOrReplaceTempView("SPO")
    result=spark.sql("select source from SPO")
    result.show(5)


    data.take(1)

    # Créez un DataFrame contenant le nombre de liens sortants pour chaque page
    outdegrees = data.groupBy("source").count().withColumnRenamed("source", "page").withColumnRenamed("count", "outDegree")
    outdegrees = apply_partitioning(outdegrees, "page")

    # Définissez le nombre d'itérations pour le calcul du PageRank
    max_iterations = int(sys.argv[2])
    damping_factor = 0.85

    # Initialisation du PageRank en attribuant à chaque page une valeur de départ
    initial_pagerank = 1.0

    # Créez un DataFrame contenant les valeurs de PageRank initiales
    pagerank = outdegrees.withColumn("pagerank", col("outDegree") / initial_pagerank)
    pagerank = apply_partitioning(pagerank, "page")

    pagerank.show(5,truncate=100)

    # Rejoignez le DataFrame pagerank avec le DataFrame data pour calculer la contribution à partir des liens entrants
    contrib = data.join(pagerank, data.target == pagerank.page, "left").select("source", "pagerank")

    new_pagerank = contrib.groupBy("source").sum("pagerank").withColumnRenamed("source", "page").withColumnRenamed("sum(pagerank)", "pagerank")

    # Joignez le DataFrame "new_pagerank" avec le DataFrame "outdegrees" pour obtenir les "outDegree" appropriés
    pagerank = new_pagerank.join(outdegrees, new_pagerank.page == outdegrees.page, "left").select(new_pagerank.page, new_pagerank.pagerank, outdegrees.outDegree)

    # Appliquez la formule du PageRank
    pagerank = pagerank.withColumn("pagerank", (1 - damping_factor) + damping_factor * col("pagerank") / col("outDegree"))
    pagerank.show(5)

    # quand le chat dit des bétises...
    # Rejoignez le DataFrame pagerank avec le DataFrame data pour calculer la contribution à partir des liens entrants
    """
    contrib = data.join(pagerank, data.target == pagerank.page, "left").select("source", "pagerank")
    contrib.show(2,truncate=100)

    # Calculez le nouveau PageRank
    pagerank = contrib.groupBy("source").sum("pagerank").withColumnRenamed("source", "page").withColumnRenamed("sum(pagerank)", "pagerank")
    pagerank.show(2)

    # Appliquez la formule du PageRank
    pagerank = pagerank.withColumn("pagerank", (1 - damping_factor) + damping_factor * col("pagerank") /  col("outDegree"))
    #pagerank.show(2)

    """

    # Define window for partitioned computation
    window_spec = Window.partitionBy("source") if partitionBy else None

    debut = time.time()

    # Effectuez des itérations pour calculer le PageRank



    for iteration in range(max_iterations):
    # Rejoignez le DataFrame pagerank avec le DataFrame data pour calculer la contribution à partir des liens entrants
        contrib = data.join(pagerank, data.target == pagerank.page, "left").select("source", "pagerank")

        new_pagerank = contrib.groupBy("source").agg(sql_sum("pagerank").alias("pagerank")).withColumnRenamed("source", "page")
        
        new_pagerank = apply_partitioning(new_pagerank, "page")

        # Joignez le DataFrame "new_pagerank" avec le DataFrame "outdegrees" pour obtenir les "outDegree" appropriés
        pagerank = new_pagerank.join(outdegrees, new_pagerank.page == outdegrees.page, "left").select(new_pagerank.page, new_pagerank.pagerank, outdegrees.outDegree).withColumn("pagerank", (1 - damping_factor) + damping_factor * col("pagerank") / col("outDegree"))

        pagerank = apply_partitioning(pagerank, "page")

        # Appliquez la formule du PageRankp
        print(pagerank)


    # Affichez les résultats
    pagerank.select("page", "pagerank").show()
    fin = time.time()
    print(f"Temps d'exécution : {fin-debut} secondes")


    # Convert the final ranks RDD to a DataFrame
    ranks_df = pagerank.select("page", "pagerank").toDF("page", "pagerank")

    # Try to get PATH_BUCKET from Spark config first, then fall back to os.getenv
    bucket_path = spark.conf.get("spark.executorEnv.PATH_BUCKET", os.getenv("PATH_BUCKET"))
    bucket_path = os.path.join(bucket_path, "out/")

    # Save the DataFrame to GCS as a CSV file
    ranks_df.write.mode("overwrite").csv(bucket_path)

    # Arrêtez la session Spark
    spark.stop()


