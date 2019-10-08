#!/bin/bash

if [ $# -ne 2 ]; then
    echo "run.sh url.list dir"
    exit 1;
fi

youtube_dl=/home/dophist/work/git/ASR_TIOBE/bin/youtube-dl

url_list=$1
dir=$2

rm -rf $dir && mkdir -p $dir/{raw,wav}
cp $url_list config.txt $dir/

cd $dir
$youtube_dl \
    --config-location config.txt \
    --batch-file url.list \
    --output "raw/%(title)s.%(ext)s" \
    --exec 'ffmpeg -i {} -ac 1 -ar 16000 wav/`basename {}`'

cd -
