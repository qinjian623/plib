#!/bin/bash
# Author: Jian QIN(qinjian623@gmail.com)


while true
do
    for i in `ssh 106.186.22.139 'ls ~/archive'`
    do
        echo $i
        scp 106.186.22.139:~/archive/$i ./archive/ &&
        ssh 106.186.22.139 "rm -f ~/archive/$i"
    done
    echo "Sleeping"
    sleep 1800
done
