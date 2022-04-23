#!/bin/bash

if [ $# -lt 1 ]; then
	echo "go.sh <txtfile> [<txtfile>...]"
	exit
fi

for file in $@; do
	echo "$file"
	base=`basename $file .txt`
	dir=`dirname $file`
	cp $file jptest.txt
	python3.8 wordnet_3gram.py
	cp jptest_node.csv ${dir}/${base}_node.csv
	cp jptest_edge.csv ${dir}/${base}_edge.csv
	cp jptest.png ${dir}/${base}.png
done

