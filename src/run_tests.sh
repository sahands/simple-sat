#!/usr/bin/env bash
for TEST_FILE in tests/w44/*.in
do
    echo $TEST_FILE
    python sat.py $1 --input $TEST_FILE
done
