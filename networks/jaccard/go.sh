#!/bin/bash

if [ $# -lt 1 ]; then
	echo "go.sh <txtfile> [<txtfile>...]"
	exit
fi

for file in $@; do
	echo "$file"
	base=`basename $file .txt`
	cp $file jptest.txt
	python3.8 wordnet_mecab.py
	cp jptest_node.csv ${base}_node.csv
	cp jptest_edge.csv ${base}_edge.csv
	cp jptest.png ${base}.png
done

