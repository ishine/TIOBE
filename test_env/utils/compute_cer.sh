if [ $# -ne 1 ]; then
  echo "compute_cer.sh <result_dir>"
  echo "e.g.: sh AISHELL-2_iOS_test__201910"
  echo "assume raw_rec.txt and trans.txt in result_dir"
  exit 1;
fi

COMPUTE_WER=`readlink -f ~/work/kaldi/src/bin/compute-wer`
ALIGN_TEXT=`readlink -f ~/work/kaldi/src/bin/align-text`

dir=$1

echo "-- <preparing reference"
python3 ../../utils/cn_tn.py --has_key --to_upper $dir/trans.txt $dir/tmp.ref_tn.txt  # TN
python3 ../../utils/split_to_char.py $dir/tmp.ref_tn.txt $dir/ref.txt
echo "-- done>"

echo "-- <preparing recognition text"
python3 ../../utils/cn_tn.py --has_key --to_upper $dir/raw_rec.txt $dir/tmp.rec_tn.txt
python3 ../../utils/split_to_char.py $dir/tmp.rec_tn.txt $dir/rec.txt
grep -v $'\t$' $dir/rec.txt > $dir/rec_present.txt # filter away empty recognition result
rm $dir/tmp.*
echo "-- done>"

echo "-- <computing CER and text alignment"
$COMPUTE_WER --mode=present --text=true ark,t:$dir/ref.txt ark,t:$dir/rec.txt >& $dir/CER
$ALIGN_TEXT ark,t:$dir/ref.txt ark,t:$dir/rec.txt ark,t:$dir/ALIGN >& $dir/log.align

$COMPUTE_WER --mode=present --text=true ark,t:$dir/ref.txt ark,t:$dir/rec_present.txt >& $dir/CER_present
$ALIGN_TEXT ark,t:$dir/ref.txt ark,t:$dir/rec_present.txt ark,t:$dir/ALIGN_present >& $dir/log.align_present
echo "-- done>"

echo "============================"
cat $dir/CER | sed -e "s:\%WER:\%CER:g"
echo "============================"
echo "============================"
cat $dir/CER_present | sed -e "s:\%WER:\%CER:g"
echo "============================"

