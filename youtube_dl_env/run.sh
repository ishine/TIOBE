#!/bin/bash

if [ $# -ne 2 ]; then
    echo "run.sh <url.list> <dir>"
    echo "  e.g.: run.sh urls.txt test_201909"
    exit 1;
fi

youtube_dl=~/work/TIOBE/youtube_dl_env/bin/youtube-dl

url_list=$1
dir=$2

rm -rf $dir && mkdir -p $dir/{raw,wav}

cp $url_list $dir/url.list
cp config.txt $dir/config.txt


cd $dir
$youtube_dl \
    --config-location config.txt \
    --batch-file url.list \
    --output "raw/%(id)s__%(title)s.%(ext)s" \
    --exec 'ffmpeg -i {} -ac 1 -ar 16000 wav/`basename {}`'
cd -

