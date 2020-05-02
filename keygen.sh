#!/bin/bash

echo 'Enter personnel name: '
read name
echo 'Enter their attributes: '
read attributes

echo 'generating key from given attributes...'
keypath="./cpabe-keys/${name}_priv_key"
cpabe-keygen -o $keypath ./cpabe-keys/pub_key ./cpabe-keys/master_key $attributes
echo 'DONE.'
