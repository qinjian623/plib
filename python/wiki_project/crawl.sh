#!/bin/bash
# Author: Jian QIN(qinjian623@gmail.com)

data_dir='./data/'
title_dir='./links/'
achive_dir='./archive/'
function get_page {
    echo $i
    wget -i $title_dir$1 -P $data_dir$1
}

function achive_pages {
    tar -czf $achive_dir$1 $data_dir$1
    rm -Rf $data_dir$1
}


# #############################################
# # Dowloaded_pages
# #############################################
# declare -A downloaded_pages

# for downloaded_page in `ls $data_dir`
# do
#     downloaded_pages[$downloaded_page]=1
# done


#############################################
# Multi-process Control
#############################################
tmp_fifofile='/tmp/tmpFilewiki'
mkfifo $tmp_fifofile      # 新建一个fifo类型的文件
exec 6<>$tmp_fifofile      # 将fd6指向fifo类型
rm $tmp_fifofile
threads_number=10

for i in `seq $threads_number`
do 
    echo >&6
    echo $i
done 

for title in `ls $title_dir`
do
    read -u6
    {
        get_page $title
        achive_pages $title
        echo >&6
    }&
done

wait
exec 6>&-
echo "ALL DONE"
