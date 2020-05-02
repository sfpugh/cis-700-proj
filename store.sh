#!/bin/bash

echo 'Enter DCM file name:'
read DCM_FILE

python image_store_protocol.py $DCM_FILE

echo 'DONE.'
