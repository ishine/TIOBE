#!/bin/bash

if [ $# -ne 1 ]; then
    echo "run.sh <dir>"
    echo "  e.g.: run.sh test_201909"
    echo "  pre-defined test_201909/url.list are required."
    exit 1;
fi

dir=$1

mkdir -p $dir/{raw,wav}

cd $dir

#annie -o raw -p `cat url.list`  # for play list urls
annie -o raw `cat url.list` # for video urls

for x in `ls raw/*`; do
    fext=`basename $x`
    f=${fext%.*}
    ffmpeg -i "$x" -ac 1 -ar 16000 wav/${f}.wav
done

cd -
