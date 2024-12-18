#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
import re
import sys
from operator import add
from typing import Iterable, Tuple

from pyspark.resultiterable import ResultIterable
from pyspark.sql import SparkSession

import os


# removed typing for compatibility with Spark 3.1.3
# typing ok with spark 3.3.0

def computeContribs(urls, rank) :
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls) :
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[2]


if __name__ == "__main__":

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    partitionBy = sys.argv[4].lower() == "true"
    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...

    # Define number of partitions
    num_partitions = 10

    # Load input file
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    if partitionBy : 
    # Initialize `links` with a partitioner and cache it
        links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().partitionBy(num_partitions).cache()

        # Initialize ranks and partition it
        ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0)).partitionBy(num_partitions)
    else : 
        links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

        # Initialize ranks and partition it
        ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))
          

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: computeContribs(
            url_urls_rank[1][0], url_urls_rank[1][1]  # type: ignore[arg-type]
        ))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)


    # Collect results
    #for (link, rank) in ranks.collect():
    #    print("%s has rank: %s." % (link, rank))

    # Convert the final ranks RDD to a DataFrame
    ranks_df = ranks.toDF(["URL", "Rank"])

    # Try to get PATH_BUCKET from Spark config first, then fall back to os.getenv
    bucket_path = spark.conf.get("spark.executorEnv.PATH_BUCKET", os.getenv("PATH_BUCKET"))
    bucket_path = os.path.join(bucket_path, "out/" + sys.argv[3]+ "/")

    # Save the DataFrame to GCS as a CSV file
    ranks_df.write.mode("overwrite").csv(bucket_path)

    spark.stop()
