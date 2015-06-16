#!bash
# $1 is filename  $2 is description $3 is link
for i in `seq 445`
do
    echo "Downloading page: http://thecodinglove.com/"$i
    wget -q http://thecodinglove.com/page/$i -O page.html
    echo "Downloading gifs of current page."
    sed -n "s/.*<a href=\"http:\/\/thecodinglove.com\/post\/[0-9]*\/\([^\"]*\)\">/\1:::/gp" page.html | sed "s/ *<div.*\(http:\/\/tclhost.com\/.*\.gif\).*/\1/g" | sed "s/<.*>/:::/g" |awk -F":::" '{system("wget -q "$3" -O "$1".gif && echo "$2":::"$3 ">> index.txt")}'
done
