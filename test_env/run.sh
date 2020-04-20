service_list="aliyun baidu google iflytek sogou tencent yitu microsoft"
testset_list="AISHELL-2_iOS_test cctv_news"
max_num_utts=10000

#----------------------------
date=`date +%Y%m%d`
RESULT=`readlink -f result`
DATASET=`readlink -f dataset`

for x in $service_list; do
    cd service/$x
    for y in $testset_list; do
        echo "==>Testing Service:$x TEST_SET:$y DATE:$date NUM_UTTS:$max_num_utts"
        job=${date}__${x}__${y}__${max_num_utts}
        mkdir -p $RESULT/$job
        nohup sh ../../utils/test.sh $max_num_utts $DATASET/$y $RESULT/$job >& $RESULT/$job/log.test &
    done
    cd -
done
wait
echo "Done"

