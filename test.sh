for TEST_FILE in test_input/w44/*.in
do
    echo $TEST_FILE
    python sat.py $1 --input $TEST_FILE
done
