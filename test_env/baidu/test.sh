if [ $# -ne 1 ]; then
  echo "test.sh <dataset_dir>"
  echo "  assume wav.scp trans.txt in dataset_dir"
  exit -1;
fi

dir=`readlink -f $1`
max=5000

awk -v d=$dir '{print $1"\t"d"/"$2}' $dir/wav.scp | head -n $max >  wav.scp

# rec result are stored in "trans.txt"
python3 rest_api.py wav.scp trans.txt
