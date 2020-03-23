service_list="aliyun baidu google iflytek tencent yitu"
test_set_list="cctv_news"
date=20200323
max_num_utts=10000
RESULT_DIR=`readlink -f RESULT_DATA`
DATASET_DIR=`readlink -f ../dataset`

for service in $service_list; do
    cd $service
    pwd
    for test_set in $test_set_list; do
        echo "==> Testing ASR:$service TEST_SET:$test_set DATE:$date NUM_UTTS:$max_num_utts"
        dir_name=${service}__${test_set}__${date}__${max_num_utts}
        sh run.sh $max_num_utts $DATASET_DIR/$test_set $RESULT_DIR/$dir_name
    done
    cd -
done
