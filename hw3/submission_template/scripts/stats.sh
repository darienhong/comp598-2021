#!/bin/bash 
wc -l < $1
head -n 1 $1
tail -n 10000 $1 | grep -c -i 'potus'
sed -n '100,200p' $1 | grep -c 'fake'
