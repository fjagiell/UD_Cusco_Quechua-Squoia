for i in *.conllu; do
    train=`ls -l *.conllu | grep -v $test` | tr '\n' ' '`;
    cat $train > train.$test
    cp $test test.$test
    echo "$test $train"
    udpipe --train $test".train.udpipe" < $test".train"
    udpipe --parse $test".test" > $test".output"
    conllu_evaluate.py $test".test" $test".output"
done
