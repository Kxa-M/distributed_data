#!/bin/bash

## En local ->
## pig -x local -

## en dataproc...

## copy data

#$1 links file  | $2 name cluster | $3 number workers | $4 number of iterations

gsutil cp $1 $PATH_BUCKET/

## copy pig code
gsutil cp pagerank-notype.py $PATH_BUCKET/

## Clean out directory
gsutil rm -rf $PATH_BUCKET/out/$2
#gsutil rm -rf gs://small_page_links/out


## create the cluster
gcloud dataproc clusters create $2 --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers $3 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project $PROJECT_NAME  --labels=goog-ops-agent-policy=v2-x86-template-1-3-0,goog-ec-src=vm_add-gcloud --reservation-affinity=any


## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster $2 --properties=spark.executorEnv.PATH_BUCKET=$PATH_BUCKET,spark.driverEnv.PATH_BUCKET=$PATH_BUCKET $PATH_BUCKET/pagerank-notype.py  -- $PATH_BUCKET/$1 $4 $2

## access results
#gsutil cat gs://tp_scale_data_m2/out/part-r-00000

## delete cluster...
gcloud dataproc clusters delete $2 --region europe-west1

