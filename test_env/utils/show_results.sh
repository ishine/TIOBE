flist=`find . -name "CER"`

for f in $flist; do
    echo $f
    cat $f | sed -e "s:\%WER:\%CER:g" | grep "CER"
    echo ""
done
