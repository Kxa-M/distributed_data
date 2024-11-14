#!/bin/bash

## En local ->
## pig -x local -

## en dataproc...

## copy data
# gsutil cp gs://public_lddm_data/small_page_links.nt $PATH_BUCKET
# gsutil cp gs://public_lddm_data/page_links_en.nt.bz2 $PATH_BUCKET



#$1 links file  | $2 name cluster | $3 number workers | $4 number of iterations


## copy pig code
gsutil cp $1 $PATH_BUCKET/
gsutil cp pagerank-df.py $PATH_BUCKET/


## Clean out directory
gsutil rm -rf $PATH_BUCKET/out/$2


## create the cluster
#gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project $PROJECT_NAME --labels=goog-ops-agent-policy=v2-x86-template-1-3-0,goog-ec-src=vm_add-gcloud --reservation-affinity=any
gcloud dataproc clusters create $2 --enable-component-gateway --region europe-west1 --zone europe-west1-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers $3 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project $PROJECT_NAME --labels=goog-ops-agent-policy=v2-x86-template-1-3-0,goog-ec-src=vm_add-gcloud --reservation-affinity=any


## run
## (suppose that out directory is empty !!)
#gcloud dataproc jobs submit pyspark --region europe-west1 --cluster cluster-a35a --properties=spark.executorEnv.PATH_BUCKET=$PATH_BUCKET,spark.driverEnv.PATH_BUCKET=$PATH_BUCKET $PATH_BUCKET/pagerank-df.py -- $PATH_BUCKET/small_page_links.nt 3
gcloud dataproc jobs submit pyspark --region europe-west1 --cluster $2 --properties=spark.executorEnv.PATH_BUCKET=$PATH_BUCKET,spark.driverEnv.PATH_BUCKET=$PATH_BUCKET $PATH_BUCKET/pagerank-df.py -- $PATH_BUCKET/$1 $4 $2 $5
## access results
#gsutil cat gs://distributed_data/out/pagerank_data_10/part-r-00000

## delete cluster...
gcloud dataproc clusters delete $2 --region europe-west1

