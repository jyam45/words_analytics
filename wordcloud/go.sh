#!/bin/bash

if [ $# -lt 1 ]; then
	echo "./go.sh <textfile> ..."
	exit
fi


for file in $@; do
	dir=`dirname $file`
	name=`basename $file .txt`
	cp $file jptest.txt
	python3 wordcloud_mecab.py
	cp jptest.png $dir/$name.png
done
