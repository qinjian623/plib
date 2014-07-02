#!/bin/bash
data_dir='/home/qin/Documents/wiki/'
title_file='/home/qin/Documents/zhwiki'

function get_page {
    echo $1
    wget "https://zh.wikipedia.org/zh-cn/$1" -O $data_dir$1
}

declare -A downloaded_pages

for downloaded_page in `ls $data_dir`
do
    downloaded_pages[$downloaded_page]=1
done

# for i in ${!downloaded_pages[@]}
# do
#      echo 
# done

tmp_fifofile='/tmp/tmpFilewiki'
mkfifo $tmp_fifofile      # 新建一个fifo类型的文件
exec 6<>$tmp_fifofile      # 将fd6指向fifo类型
rm $tmp_fifofile
threads_number=400

for i in `seq $threads_number`
do 
    echo >&6
    echo $i
done 

for title in `cat $title_file`
do
    v=${downloaded_pages[$title]}
    if [ "$v" = "1" ]
    then
        continue
    else
        read -u6
        {
            get_page $title
            echo >&6
        }&
    fi
done
wait
exec 6>&-
echo "ALL DONE"
