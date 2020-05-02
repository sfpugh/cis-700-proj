#!/bin/bash

echo 'Enter directory for results: '
read RESULTS_DIR
mkdir -p $RESULTS_DIR

echo 'Specify private key file path: '
read PRIV_KEY

python query_protocol.py $PRIV_KEY $RESULTS_DIR

i=1
FILES="${RESULTS_DIR}/.*.cpabe"
for f in $FILES
do
    O_FILE="${RESULTS_DIR}/result${i}.DCM"
    cpabe-dec -o $O_FILE  ./cpabe-keys/pub_key $PRIV_KEY $f
    
    if test -f "$O_FILE"; then
        ((i=i+1))
    fi
done

echo 'DONE.'
