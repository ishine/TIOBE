if [ $# -ne 2 ]; then
  echo "recognize.sh wav.scp <working_dir>"
  exit 1;
fi

scp=$1
dir=$2

sh update_token.sh
./asr_api.py $scp $dir/raw_rec.txt >& $dir/log
