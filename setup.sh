#!/bin/bash

echo 'setting up abe system...'
cpabe-setup
mkdir cpabe-keys
mv pub_key master_key cpabe-keys
echo 'DONE.'
