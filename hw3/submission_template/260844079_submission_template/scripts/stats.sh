#!/bin/bash
if [[ $(wc -l < $1 ) -lt 10000 ]]
then 
	echo "The file should have at least 10,000 lines."
	exit 1 
fi 
wc -l < $1
head -n 1 $1
tail -n 10000 $1 | grep -c -i 'potus'
sed -n '100,200p' $1 | grep -c '\bfake\b'
