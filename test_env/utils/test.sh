if [ $# -ne 3 ]; then
  echo "test.sh <max_num_utts> <testset_dir> <result_dir>"
  echo "e.g.: sh test.sh 5000 TESTSET_201910 RES_201910"
  echo "  assume wav.scp trans.txt in dataset_dir"
  exit 1;
fi

n=$1
testset=`readlink -f $2`
dir=$3

COMPUTE_WER=`readlink -f ~/work/kaldi/src/bin/compute-wer`
ALIGN_TEXT=`readlink -f ~/work/kaldi/src/bin/align-text`

if [ ! -f ${testset}/wav.scp ] || [ ! -f ${testset}/trans.txt ]; then
    echo "ERROR: missing wav.scp or trans.txt in test set"
    exit 1;
fi

mkdir -p $dir

echo "-- <preparing wav list with abs paths"
awk -v d=$dir '{print $1"\t"d"/"$2}' ${testset}/wav.scp | head -n $n > $dir/wav.scp
echo "-- done>"

# prepare ref (Text Norm & Tokenization to char)
echo "-- <preparing reference"
head -n $n ${testset}/trans.txt > $dir/tmp.ref.txt
python3 ../utils/cn_tn.py --has_key $dir/tmp.ref.txt $dir/tmp.ref_tn.txt  # TN
python3 ../utils/split_to_char.py $dir/tmp.ref_tn.txt $dir/ref.txt
echo "-- done>"

# prepare rec (Text Norm & Tokenization to char)
echo "-- <recognizing"
python3 asr_api.py $dir/wav.scp $dir/raw_rec.txt >& $dir/asr.log
python3 ../utils/cn_tn.py --has_key $dir/raw_rec.txt $dir/tmp.rec_tn.txt
python3 ../utils/split_to_char.py $dir/tmp.rec_tn.txt $dir/rec.txt
rm $dir/tmp.*
echo "-- done>"

# get CER and ALIGN
echo "-- <computing CER and text alignment"
$COMPUTE_WER --mode=present --text=true ark,t:$dir/ref.txt ark,t:$dir/rec.txt >& $dir/CER
$ALIGN_TEXT ark,t:$dir/ref.txt ark,t:$dir/rec.txt ark,t:$dir/ALIGN >& $dir/align.log
echo "-- done>"
echo "============================"
cat $dir/CER | sed -e "s:\%WER:\%CER:g"
echo "============================"

