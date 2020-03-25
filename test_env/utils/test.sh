if [ $# -ne 3 ]; then
  echo "test.sh <max_num_utts> <testset_dir> <result_dir>"
  echo "e.g.: sh test.sh 5000 TESTSET_201910 RES_201910"
  echo "  assume wav.scp trans.txt in dataset_dir"
  exit 1;
fi

n=$1
testset=`readlink -f $2`
dir=$3

stage=0

COMPUTE_WER=`readlink -f ~/work/kaldi/src/bin/compute-wer`
ALIGN_TEXT=`readlink -f ~/work/kaldi/src/bin/align-text`

if [ ! -f ${testset}/wav.scp ] || [ ! -f ${testset}/trans.txt ]; then
    echo "ERROR: missing wav.scp or trans.txt in test set"
    exit 1;
fi

mkdir -p $dir

echo "-- <preparing wav list with abs paths & trans"
awk -v d=$testset '{print $1"\t"d"/"$2}' ${testset}/wav.scp | head -n $n > $dir/wav.scp
head -n $n ${testset}/trans.txt > $dir/trans.txt
echo "-- done>"

if [ $stage -le 9 ]; then
echo "-- <recognizing"
./asr_api.py $dir/wav.scp $dir/raw_rec.txt >& $dir/asr.log
echo "-- done>"
fi

echo "-- <Getting cer"
sh ../utils/cer.sh $dir >& $dir/cer.log
echo "-- done>"

