#$1 links file  | $2 name cluster | $3 number workers | $4 number of iterations | $5 boolean to enable partitionner

## notype

nohup bash run.sh page_links_en.nt.bz2 cluster-notype-partition-0w 0 3 true > output_pl_notype_partition_0w.log 2>&1 &
nohup bash run.sh page_links_en.nt.bz2 cluster-notype-partition-2w 2 3 true > output_pl_notype_partition_2w.log 2>&1 &
nohup bash run.sh page_links_en.nt.bz2 cluster-notype-partition-4w 4 3 true > output_pl_notype_partition_4w.log 2>&1 &

nohup bash run.sh page_links_en.nt.bz2 cluster-notype-no-partition-0w 0 3 false > output_pl_notype_no_partition_0w.log 2>&1 &
nohup bash run.sh page_links_en.nt.bz2 cluster-notype-no-partition-2w 2 3 false > output_pl_notype_no_partition_2w.log 2>&1 &
nohup bash run.sh page_links_en.nt.bz2 cluster-notype-no-partition-4w 4 3 false > output_pl_notype_no_partition_4w.log 2>&1 &


## DF

nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-partition-0w 0 3 true > output_pl_df_partition_0w.log 2>&1 &
nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-partition-2w 2 3 true > output_pl_df_partition_2w.log 2>&1 &
nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-partition-4w 4 3 true > output_pl_df_partition_4w.log 2>&1 &

nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-no-partition-0w 0 3 false > output_pl_df_no_partition_0w.log 2>&1 &
nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-no-partition-2w 2 3 false > output_pl_df_no_partition_2w.log 2>&1 &
nohup bash run-df.sh page_links_en.nt.bz2 cluster-df-no-partition-4w 4 3 false > output_pl_df_no_partition_4w.log 2>&1 &