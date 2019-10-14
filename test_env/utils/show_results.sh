flist=`find . -name "CER"`

for f in $flist; do
    echo $f
    cat $f
    echo ""
done
