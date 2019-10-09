nohup sh test.sh ../../dataset/AISHELL-2/iOS/test >& log &
sleep 5
tail -f trans.txt
