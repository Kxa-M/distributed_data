#!/bin/bash

## En local ->
## pig -x local -

## en dataproc...


## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 50 --num-workers 0 --worker-machine-type n1-standard-4 --worker-boot-disk-size 50 --image-version 2.0-debian10 --project big-data-m2


## copy data
gsutil cp small_page_links.nt gs://tp_scale_data_m2/

## copy pig code
gsutil cp dataproc.py gs://tp_scale_data_m2/

## Clean out directory
gsutil rm -rf gs://tp_scale_data_m2/out
gsutil rm -rf gs://small_page_links/out


## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pig --region europe-west1 --cluster cluster-a35a -f gs://tp_scale_data_m2/dataproc.py

## access results
#gsutil cat gs://tp_scale_data_m2/small_page_links/out/pagerank_data_1/part-r-00000

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-west1

