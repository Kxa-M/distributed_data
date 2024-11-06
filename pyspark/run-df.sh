#!/bin/bash

## En local ->
## pig -x local -

## en dataproc...

## copy data
gsutil cp gs://public_lddm_data/small_page_links.nt gs://distributed_data/
gsutil cp gs://public_lddm_data/page_links_en.nt.bz2 gs://distributed_data/

## copy pig code
gsutil cp pagerank-df.py gs://distributed_data/

## Clean out directory
gsutil rm -rf gs://distributed_data/out
gsutil rm -rf gs://small_page_links/out


## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project distributed-systems-436009


## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster cluster-a35a gs://distributed_data/pagerank-df.py  -- gs://distributed_data/page_links_en.nt.bz2 3

## access results
#gsutil cat gs://distributed_data/out/pagerank_data_10/part-r-00000

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-west1

