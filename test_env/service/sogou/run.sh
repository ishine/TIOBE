if [ $# -ne 3 ]; then
  echo "run.sh <max_num_utts> <test_set_path> <result_dir_name>"
  exit 1;
fi

max_num_utts=$1
test_set_path=$2
result_dir_name=$3

sh update_token.sh
sh ../utils/test.sh $max_num_utts $test_set_path $result_dir_name
