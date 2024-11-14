#$1 links file  | $2 name cluster | $3 number workers | $4 number of iterations

## notype

nohup bash run.sh small_page_links.nt cluster-notype-partition 2 3 > $PATH_BUCKET/output_sm_notype_partition_2w.log 2>&1 &

nohup bash run.sh small_page_links.nt cluster-notype-no-partition 0 3 > $PATH_BUCKET/output_sm_notype_no_partition_0w.log 2>&1 &

## DF

nohup bash run-df.sh small_page_links.nt cluster-df-partition 0 3 > $PATH_BUCKET/output_sm_df_partition_0w.log 2>&1 &

nohup bash run-df.sh small_page_links.nt cluster-df-no-partition 0 3 > $PATH_BUCKET/output_sm_df_no_partition_0w.log 2>&1 &