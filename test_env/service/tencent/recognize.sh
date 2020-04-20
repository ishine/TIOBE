if [ $# -ne 2 ]; then
  echo "recognize.sh wav.scp <working_dir>"
  exit 1;
fi

scp=$1
dir=$2

./asr_api.py $scp $dir/raw_rec.txt >& $dir/log
