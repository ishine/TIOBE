export GOOGLE_APPLICATION_CREDENTIALS=`readlink -f ~/work/ASR_TIOBE/test_env/google/TIOBE.json`
sh ../utils/test.sh 3 ../../dataset/AISHELL-2/iOS/test RES_AISHELL-2-IOS_20191010
