#!/bin/bash
words_file_name=$1
data_file_name=$2
temp_file_name=`tempfile`
for word in `cat $words_file_name`
do
    grep $word $data_file_name  |sed "s/$word/DD/g" >> $temp_file_name
done

awk -F'","' '{print $1}' $temp_file_name  | sort |uniq -c |sort -n -r
